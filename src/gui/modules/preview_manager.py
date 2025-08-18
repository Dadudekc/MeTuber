"""
Preview Manager Module for Dreamscape V2 Professional

Handles all preview-related functionality including frame updates,
camera adjustments, performance monitoring, and preview controls.
"""

import logging
import time
from click import edit
import cv2
from networkx import edges
import numpy as np
from collections import deque
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QThread, QElapsedTimer
from PyQt5.QtGui import QPixmap, QImage


class EffectProcessor(QThread):
    """Asynchronous effect processor with lock-free frame handling."""
    
    frame_processed = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Effect management
        self.current_effect = None
        self.current_style = None
        self.current_params = {}
        
        # PERFORMANCE OPTIMIZATION: Replace Queue with bounded deque (lock-free, drop-oldest)
        self._frames = deque(maxlen=3)
        self.processing_enabled = True
        self.frame_drop_count = 0
        
        # Performance monitoring
        self.last_process_time = time.time()
        self.process_count = 0
    
    def set_effect(self, effect, params):
        """Set the current effect to apply."""
        try:
            self.current_effect = effect
            self.current_params = params or {}
            self.logger.debug(f"Effect set: {effect}")
        except Exception as e:
            self.logger.error(f"Error setting effect: {e}")
    
    def set_style(self, style, params):
        """Set the current style to apply."""
        try:
            self.current_style = style
            self.current_params = params or {}
            self.logger.debug(f"Style set: {style}")
        except Exception as e:
            self.logger.error(f"Error setting style: {e}")
    
    def process_frame(self, frame):
        """Add frame to processing queue with smart dropping."""
        try:
            if not self.processing_enabled or frame is None:
                return
            
            # Stamp a timestamp at source (idempotent)
            if not hasattr(frame, "timestamp"):
                frame.timestamp = time.time()
            
            pre_len = len(self._frames)
            self._frames.append(frame)
            if len(self._frames) == pre_len:  # deque dropped oldest
                self.frame_drop_count += 1
                if self.frame_drop_count % 10 == 0:
                    self.logger.warning(f"⚠️ Dropped {self.frame_drop_count} frames for performance")
            
        except Exception as e:
            self.logger.error(f"Error adding frame to queue: {e}")
    
    def run(self):
        """Main processing loop with performance optimization."""
        self.logger.info("🚀 Effect processor started")
        
        while self.processing_enabled:
            try:
                if not self._frames:
                    self.msleep(1)
                    continue
                
                frame = self._frames.pop()  # take newest, implicitly drop stale
                
                # Skip if stale
                if getattr(frame, "timestamp", 0) and (time.time() - frame.timestamp) > 0.5:
                    continue
                
                # Process frame with timing budget
                t0 = time.time()
                processed_frame = self._apply_effects(frame)
                dt = time.time() - t0
                
                # Skip if processing took too long (33ms budget for 30fps target)
                if dt > 0.033:
                    self.logger.debug(f"slow frame {dt*1000:.1f}ms (skipped emit)")
                    continue
                
                # Emit processed frame
                if processed_frame is not None:
                    self.frame_processed.emit(processed_frame)
                    self.process_count += 1
                
                # Performance monitoring
                if self.process_count % 30 == 0:
                    now = time.time()
                    fps = 30.0 / max(dt, 1e-3)  # local time budget proxy
                    self.logger.info(f"📊 Effects budget: ~{fps:.1f} FPS-equivalent, last {dt*1000:.1f}ms")
                    self.process_count = 0
                
            except Exception as e:
                self.logger.exception("Error in effect processor loop")
                self.msleep(5)
        
        self.logger.info("🛑 Effect processor stopped")
    
    def _apply_effects(self, frame):
        """Apply current effects and styles to frame."""
        try:
            processed_frame = frame.copy()
            
            # Apply style if available
            if self.current_style and hasattr(self.current_style, 'apply'):
                try:
                    processed_frame = self.current_style.apply(processed_frame, self.current_params)
                except Exception as style_error:
                    self.logger.warning(f"Style application failed: {style_error}")
            
            # Apply effect if available
            if self.current_effect and hasattr(self.current_effect, 'apply'):
                try:
                    processed_frame = self.current_effect.apply(processed_frame, self.current_params)
                except Exception as effect_error:
                    self.logger.warning(f"Effect application failed: {effect_error}")
            
            return processed_frame
            
        except Exception as e:
            self.logger.error(f"Error applying effects: {e}")
            return frame
    
    def stop(self):
        """Stop the processing thread."""
        try:
            self.processing_enabled = False
            self.wait(1000)  # Wait up to 1 second for clean shutdown
            self.logger.info("✅ Effect processor stopped")
        except Exception as e:
            self.logger.error(f"Error stopping effect processor: {e}")


class PreviewManager:
    """Manages all preview-related functionality."""
    
    def __init__(self, main_window):
        """Initialize preview manager with reference to main window."""
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # Preview management
        self.preview_timer = None
        self.preview_active = False
        self.last_processed_frame = None
        
        # PERFORMANCE OPTIMIZATION: Add performance settings
        self.target_fps = 30  # Start with full performance
        self.frame_skip_count = 0
        self.max_frame_skip = 0  # Start with no frame skipping
        self.effects_active = False
        self.quality_reduction = False  # For heavy effects
        self.processing_enabled = False  # Start with effects disabled
        
        # NEW: metrics/init guards
        self._ema_fps = 0.0
        self._fps_alpha = 0.2
        self._tick_timer = QElapsedTimer()
        self._tick_timer.start()
        self.frame_count = 0
        self.last_frame_time = time.time()
        self.is_processing = False
        
        # NEW: persistent capture
        self._cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if hasattr(cv2, 'CAP_DSHOW') else cv2.VideoCapture(0)
        if self._cap and self._cap.isOpened():
            try:
                self._cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                self._native_w = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
                self._native_h = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
                self.logger.info(f"✅ Persistent capture initialized: {self._native_w}x{self._native_h}")
            except Exception as e:
                self.logger.warning(f"Failed to configure capture: {e}")
                self._native_w, self._native_h = 640, 480
        else:
            self._cap = None
            self._native_w, self._native_h = 640, 480
            self.logger.warning("⚠️ Failed to initialize persistent capture")
        
        self._last_qimage_bytes = None  # keep buffer alive
        
        # Effect processor for async processing
        self.effect_processor = EffectProcessor()
        self.effect_processor.frame_processed.connect(self._on_frame_processed)
        
        # Initialize preview timer
        self.init_preview_timer()
        
    def init_preview_timer(self):
        """Initialize preview timer with performance optimization."""
        try:
            self.logger.info("🔧 Initializing preview timer.")
            
            # PERFORMANCE OPTIMIZATION: Use target FPS instead of fixed 100ms
            interval = int(1000 / self.target_fps)  # Convert FPS to milliseconds
            
            self.preview_timer = QTimer()
            self.preview_timer.setTimerType(Qt.PreciseTimer)  # More accurate timing
            self.preview_timer.setInterval(interval)
            self.preview_timer.timeout.connect(self.update_preview)
            
            self.logger.info(f"✅ Preview timer initialized with {self.target_fps} FPS ({interval}ms)")
            
        except Exception as e:
            self.logger.error(f"Error initializing preview timer: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def pre_initialize_timer(self):
        """Pre-initialize timer for instant startup."""
        self.init_preview_timer()
        
    def update_preview(self):
        """Update preview with performance optimization."""
        try:
            # smart skip if effects heavy
            if self.effects_active and self.max_frame_skip:
                self.frame_skip_count = (self.frame_skip_count + 1) % (self.max_frame_skip + 1)
                if self.frame_skip_count != 0:
                    return
            
            # Get current frame
            frame = self.get_current_frame()
            if frame is None:
                self.logger.debug("No frame; showing fallback")
                self._display_test_frame()
                return
            
            # optional downscale once per change
            if self.quality_reduction and self.effects_active:
                h, w = frame.shape[:2]
                if w > 640:
                    scale = 640.0 / w
                    frame = cv2.resize(frame, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
                    self.logger.debug(f"🔧 Reduced frame size to {int(w*scale)}x{int(h*scale)} for performance")
            
            # CRITICAL FIX: Always update effect processor with current effects/styles
            self._update_effect_processor()
            
            # PERFORMANCE OPTIMIZATION: Route ALL frames through effect processor when enabled
            if self.processing_enabled:
                # Send frame to async effect processor
                self.effect_processor.process_frame(frame)
                self.logger.debug("🎨 Frame sent to effect processor")
            else:
                # No effects - display frame directly with camera adjustments only
                adjusted_frame = self.apply_camera_adjustments(frame)
                self.update_preview_display(adjusted_frame)
                self.logger.debug("📷 Frame displayed directly (no effects)")
            
            # FPS EMA calculation
            now = time.time()
            dt = max(now - self.last_frame_time, 1e-6)
            inst_fps = 1.0 / dt
            self._ema_fps = inst_fps if self._ema_fps == 0 else (
                self._fps_alpha * inst_fps + (1 - self._fps_alpha) * self._ema_fps
            )
            self.last_frame_time = now
            self.frame_count += 1
            
            # Update FPS display if available
            if self.frame_count % int(max(1, self.target_fps)) == 0:
                if hasattr(self.main_window, "fps_label"):
                    self.main_window.fps_label.setText(f"FPS: {self._ema_fps:.1f}")
                
        except Exception as e:
            self.logger.exception("Error updating preview")
            self._display_test_frame()
            
    def get_current_frame(self):
        """Get current frame from webcam or direct capture."""
        try:
            # When effects are enabled, get RAW frames to prevent double-processing
            if self.processing_enabled:
                # Use persistent capture for raw frames
                if self._cap and self._cap.isOpened():
                    ret, frame = self._cap.read()
                    if ret and frame is not None and getattr(frame, "size", 0) > 0:
                        return frame
                
                # Fallback to webcam manager raw frame if available
                wm = getattr(self.main_window, 'webcam_manager', None)
                if wm and hasattr(wm, "get_raw_frame"):
                    try:
                        frame = wm.get_raw_frame()
                        if frame is not None and getattr(frame, "size", 0) > 0:
                            return frame
                    except Exception:
                        self.logger.debug("Webcam manager raw frame failed", exc_info=True)
            else:
                # No effects - can use processed frames from webcam service
                wm = getattr(self.main_window, 'webcam_manager', None)
                if wm and hasattr(wm, "get_current_frame"):
                    try:
                        frame = wm.get_current_frame()
                        if frame is not None and getattr(frame, "size", 0) > 0:
                            return frame
                    except Exception:
                        self.logger.debug("Webcam manager failed", exc_info=True)
            
            # Persistent cv2 capture fallback
            if self._cap and self._cap.isOpened():
                ret, frame = self._cap.read()
                if ret and frame is not None and getattr(frame, "size", 0) > 0:
                    return frame
            
            # Fallback: return last processed frame or None
            if hasattr(self, 'last_processed_frame') and self.last_processed_frame is not None:
                return self.last_processed_frame
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting current frame: {e}")
            return None
    
    def _generate_test_frame(self):
        """Generate a test frame using vectorized operations."""
        try:
            h, w = 480, 640
            # Vectorized test frame generation
            x = np.linspace(0, 255, w, dtype=np.uint8)
            y = np.linspace(0, 255, h, dtype=np.uint8)
            xv, yv = np.meshgrid(x, y)
            frame = np.stack([xv, yv, np.full_like(xv, 128)], axis=2)
            
            # Add text overlay
            cv2.putText(frame, "No Camera Available", (50, h//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv2.putText(frame, "Check camera connection", (50, h//2 + 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200), 2)
            
            return frame
            
        except Exception as e:
            self.logger.error(f"Error generating test frame: {e}")
            return np.zeros((480, 640, 3), dtype=np.uint8)
            
    def apply_camera_adjustments(self, frame):
        """Apply camera adjustments with safe math operations."""
        try:
            if frame is None:
                return frame
            
            b = getattr(self.main_window, 'brightness_slider', None)
            c = getattr(self.main_window, 'contrast_slider', None)
            s = getattr(self.main_window, 'saturation_slider', None)
            
            if not (b and c and s):
                return frame
            
            beta = int(b.value())  # -100..100 typical
            alpha = float(c.value()) / 100.0  # 0.0..2.0
            satf = float(s.value()) / 100.0   # 0.0..2.0
            
            if beta != 0 or alpha != 1.0:
                frame = cv2.convertScaleAbs(frame, alpha=max(0.0, alpha), beta=beta)
            
            if satf != 1.0:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # scale S channel safely
                s_chan = hsv[:, :, 1].astype(np.float32) * max(0.0, satf)
                np.clip(s_chan, 0, 255, out=s_chan)
                hsv[:, :, 1] = s_chan.astype(np.uint8)
                frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
            return frame
            
        except Exception as e:
            self.logger.exception("Error applying camera adjustments")
            return frame
    
    def apply_captioner_overlay(self, frame):
        """Apply captioner overlay to the frame if active."""
        try:
            if frame is None:
                return frame
                
            # Check if captioner is available and active
            if (hasattr(self.main_window, 'ui_components') and 
                hasattr(self.main_window.ui_components, 'audio_captioner_controls')):
                
                audio_controls = self.main_window.ui_components.audio_captioner_controls
                
                if audio_controls and audio_controls.is_active():
                    captioner_manager = audio_controls.get_captioner_manager()
                    
                    if captioner_manager:
                        # Render captioner overlay
                        frame_with_captions = captioner_manager.render_frame(frame)
                        if frame_with_captions is not None:
                            return frame_with_captions
            
            return frame
            
        except Exception as e:
            self.logger.error(f"Error applying captioner overlay: {e}")
            return frame
            
    def update_preview_display(self, frame):
        """Update the preview display with a frame using safe buffer handling."""
        try:
            if frame is None or not hasattr(frame, "shape") or frame.size == 0:
                return
            
            # Convert BGR to RGB for Qt
            if frame.ndim == 3 and frame.shape[2] == 3:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                rgb = frame
            
            h, w = rgb.shape[:2]
            
            # Own the memory: make contiguous bytes and keep a ref
            self._last_qimage_bytes = rgb.tobytes()
            qimg = QImage(self._last_qimage_bytes, w, h, w*3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            
            # Scale pixmap to fit preview label
            label = getattr(self.main_window, "preview_label", None)
            if label:
                scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label.setPixmap(scaled)
                label.raise_()
                label.show()
                
                self.logger.debug(f"Frame displayed: {w}x{h} -> {scaled.width()}x{scaled.height()}")
            else:
                self.logger.debug("Preview label not available")
                
        except Exception as e:
            self.logger.exception("Error updating preview display")
            
    def get_preview_size(self):
        """Get the current preview size."""
        try:
            if hasattr(self.main_window, 'preview_label') and self.main_window.preview_label:
                return self.main_window.preview_label.size()
            return None
        except Exception as e:
            self.logger.error(f"Error getting preview size: {e}")
            return None
    
    def update_performance_indicators(self):
        """Update performance indicators in the UI."""
        try:
            # Update FPS display using our EMA calculation
            if hasattr(self, '_ema_fps') and hasattr(self.main_window, 'fps_label'):
                self.main_window.fps_label.setText(f"FPS: {self._ema_fps:.1f}")
            
            # Update other performance indicators
            self.update_cpu_memory_gpu()
            
        except Exception as e:
            self.logger.error(f"Error updating performance indicators: {e}")
            
    def update_cpu_memory_gpu(self):
        """Update CPU/Memory/GPU indicators with lightweight monitoring."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.0)  # non-blocking
            if hasattr(self.main_window, 'cpu_label'):
                self.main_window.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
            
            mem = psutil.virtual_memory()
            if hasattr(self.main_window, 'memory_label'):
                self.main_window.memory_label.setText(f"Memory: {mem.used // (1024*1024)} MB")
            
            if hasattr(self.main_window, 'gpu_label'):
                self.main_window.gpu_label.setText("GPU: n/a")
                
        except Exception:
            # avoid noisy logs here
            pass
    
    def _on_frame_processed(self, processed_frame):
        """Callback for when effect processor finishes processing a frame."""
        try:
            if processed_frame is not None:
                self.last_processed_frame = processed_frame
                self.update_preview_display(processed_frame)
                self.logger.debug("✅ Frame processed and displayed")
            else:
                self.logger.warning("⚠️ Effect processor returned None frame")
        except Exception as e:
            self.logger.exception("Error handling processed frame")
    
    def _update_effect_processor(self):
        """Update effect processor with current effects and styles."""
        try:
            # Get current effect from plugin manager
            if hasattr(self.main_window, 'plugin_manager') and self.main_window.plugin_manager:
                current_effect = self.main_window.plugin_manager.get_current_effect()
                if current_effect:
                    self.effect_processor.set_effect(current_effect, {})
                    self.logger.debug(f"🎨 Effect processor updated with: {current_effect}")
            
            # Get current style from main window (this is what's actually being used)
            if hasattr(self.main_window, 'current_style') and self.main_window.current_style:
                current_style = self.main_window.current_style
                if hasattr(current_style, 'apply'):
                    self.effect_processor.set_style(current_style, {})
                    self.logger.debug(f"🎨 Effect processor updated with style: {current_style.name if hasattr(current_style, 'name') else 'Unknown'}")
                    
        except Exception as e:
            self.logger.exception("Error updating effect processor")
    
    def on_preview_size_changed(self, size_text):
        """Handle preview size change."""
        try:
            self.logger.info(f"Preview size changed to: {size_text}")
            # Preview will be updated on next timer tick
        except Exception as e:
            self.logger.error(f"Error handling preview size change: {e}")
            
    def on_zoom_changed(self, zoom_text):
        """Handle preview zoom change."""
        try:
            # Zoom will be applied on next frame update
            pass
        except Exception as e:
            self.logger.error(f"Error handling zoom change: {e}")
            
    def on_performance_changed(self):
        """Handle performance setting changes."""
        try:
            # Stop current timer
            if self.preview_timer and self.preview_timer.isActive():
                self.preview_timer.stop()
                
            # Get new settings
            if hasattr(self.main_window, 'fps_combo'):
                fps_text = self.main_window.fps_combo.currentText()
                fps_map = {
                    "15 FPS": 67,   # 1000ms / 15
                    "30 FPS": 33,   # 1000ms / 30
                    "60 FPS": 17,   # 1000ms / 60
                    "120 FPS": 8    # 1000ms / 120
                }
                interval = fps_map.get(fps_text, 33)
                self.preview_timer.setInterval(interval)
                
            # Restart timer if processing
            if self.is_processing:
                self.preview_timer.start()
                
        except Exception as e:
            self.logger.error(f"Error handling performance change: {e}")
            
    def toggle_effects(self, enabled):
        """Toggle effects processing on/off with performance optimization."""
        try:
            self.processing_enabled = bool(enabled)
            self.effects_active = bool(enabled)
            
            if enabled:
                # Effects enabled - use optimized effect processor
                self.target_fps = 15  # Lower FPS for effects
                self.max_frame_skip = 1  # Skip every other frame for heavy effects
                self.quality_reduction = True  # Reduce quality for performance
                
                # CRITICAL: Disable webcam service style application to prevent double-processing
                if hasattr(self.main_window, 'webcam_manager') and self.main_window.webcam_manager:
                    if hasattr(self.main_window.webcam_manager.webcam_service, 'disable_style_processing'):
                        self.main_window.webcam_manager.webcam_service.disable_style_processing()
                        self.logger.info("🔧 Disabled webcam service style processing (using effect processor)")
                
                self.logger.info("🎨 Effects enabled - using optimized effect processor")
            else:
                # Effects disabled - restore full performance
                self.target_fps = 30  # Full FPS
                self.max_frame_skip = 0  # No frame skipping
                self.quality_reduction = False  # Full quality
                
                # Re-enable webcam service style processing
                if hasattr(self.main_window, 'webcam_manager') and self.main_window.webcam_manager:
                    if hasattr(self.main_window.webcam_manager.webcam_service, 'enable_style_processing'):
                        self.main_window.webcam_manager.webcam_service.enable_style_processing()
                        self.logger.info("🔧 Re-enabled webcam service style processing")
                
                self.logger.info("🎨 Effects disabled - restored full performance")
            
            # Update timer interval
            if self.preview_timer:
                self.preview_timer.setInterval(int(1000 / self.target_fps))
            
            # Start/stop effect processor
            if enabled and not self.effect_processor.isRunning():
                self.effect_processor.start()
                self.logger.info("✅ Effect processor started")
            elif not enabled and self.effect_processor.isRunning():
                self.effect_processor.stop()
                self.logger.info("✅ Effect processor stopped")
            
            self.logger.info(f"🎨 Effects {'enabled' if enabled else 'disabled'} - Target FPS: {self.target_fps}")
            
        except Exception as e:
            self.logger.error(f"Error toggling effects: {e}")
    
    def update_performance_settings(self, target_fps=None, frame_skip=None, quality_reduction=None):
        """Update performance settings dynamically."""
        try:
            if target_fps is not None:
                self.target_fps = target_fps
                if self.preview_timer:
                    new_interval = int(1000 / self.target_fps)
                    self.preview_timer.setInterval(new_interval)
                    self.logger.info(f"🔧 Performance: Target FPS updated to {target_fps}")
            
            if frame_skip is not None:
                self.max_frame_skip = frame_skip
                self.logger.info(f"🔧 Performance: Frame skip updated to {frame_skip}")
            
            if quality_reduction is not None:
                self.quality_reduction = quality_reduction
                self.logger.info(f"🔧 Performance: Quality reduction {'enabled' if quality_reduction else 'disabled'}")
                
        except Exception as e:
            self.logger.error(f"Error updating performance settings: {e}")
    
    def get_performance_stats(self):
        """Get current performance statistics."""
        try:
            current_time = time.time()
            if hasattr(self, 'last_frame_time') and hasattr(self, 'frame_count'):
                time_diff = current_time - self.last_frame_time
                if time_diff > 0:
                    current_fps = self.frame_count / time_diff
                else:
                    current_fps = 0
            else:
                current_fps = 0
            
            return {
                'target_fps': self.target_fps,
                'current_fps': current_fps,
                'ema_fps': self._ema_fps,
                'frame_skip': self.max_frame_skip,
                'quality_reduction': self.quality_reduction,
                'effects_active': self.effects_active
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance stats: {e}")
            return {}
    
    def start_preview(self):
        """Start preview display with performance optimization."""
        try:
            self.logger.info("🚀 Starting preview display...")
            
            # Start webcam processing for preview
            if hasattr(self.main_window, 'webcam_manager'):
                self.main_window.webcam_manager.start_processing()
                self.logger.info("✅ Webcam processing started successfully")
            
            # Start effect processor if effects are enabled
            if self.processing_enabled and not self.effect_processor.isRunning():
                self.effect_processor.start()
                self.logger.info("✅ Effect processor started")
            
            # Generate initial test frame
            self.logger.info("Generating initial test frame...")
            self._display_test_frame()
            self.logger.info("✅ Initial test frame displayed successfully")
            
            # Start preview timer
            if self.preview_timer:
                self.preview_timer.start()
                self.logger.info("✅ Preview timer started successfully")
                
                # Attempt to update preview immediately
                self.logger.info("Attempting to update preview...")
                self.update_preview()
                self.logger.info("✅ Preview update completed successfully")
            else:
                self.logger.error("❌ Preview timer not available")
            
            self.is_processing = True
                
        except Exception as e:
            self.logger.error(f"Error starting preview: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def _display_test_frame(self):
        """Display a test frame for debugging."""
        try:
            # Create a simple test frame
            test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            
            # Add some visual elements
            cv2.rectangle(test_frame, (100, 100), (540, 380), (0, 255, 0), 3)
            cv2.putText(test_frame, "Test Frame", (200, 250), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(test_frame, "Camera Preview", (180, 300), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Display the test frame
            self.update_preview_display(test_frame)
            
        except Exception as e:
            self.logger.error(f"Error displaying test frame: {e}")
    
    def stop_preview(self):
        """Stop the preview display."""
        try:
            self.is_processing = False
            if self.preview_timer:
                self.preview_timer.stop()
            if self.effect_processor.isRunning():
                self.effect_processor.stop()
        except Exception as e:
            self.logger.error(f"Error stopping preview: {e}")
    
    def toggle_performance_graph(self):
        """Toggle performance graph display."""
        try:
            # Implementation for performance graph toggle
            pass
        except Exception as e:
            self.logger.error(f"Error toggling performance graph: {e}")
            
    def cleanup(self):
        """Clean up preview resources."""
        try:
            self.stop_preview()
            if self._cap:
                self._cap.release()
                self._cap = None
        except Exception as e:
        
         ACP: motivational edges and coordination.
        Channels:
         Provide tests/build evidence; write concise commit messages.
            self.logger.exception("Error cleaning up preview manager")  Reuse/refactor; avoid duplication and stubs; keep edit small and cohesive.