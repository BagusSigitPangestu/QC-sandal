import cv2
import numpy as np
from typing import Tuple, Dict, List

class AdaptiveSandalMeasurement:
    def __init__(self):
        
        # ArUco configuration
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        
        # Reference distances in mm - EXACT V12
        self.reference_distances = {
            # Long distances (370mm)
            (0, 2): 370.0,
            (7, 3): 370.0,
            (6, 4): 370.0,
            # Short distances (200mm)
            (0, 6): 200.0,
            (1, 5): 200.0,
            (2, 4): 200.0
        }
        
    def detect_aruco_markers(self, image: np.ndarray) -> Tuple[Dict, np.ndarray]:
        """
        Detect and identify ArUco markers - EXACT V12
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (marker_centers_dict, annotated_image)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect ArUco markers
        corners, ids, _ = self.detector.detectMarkers(gray)
        
        marker_centers = {}
        annotated_image = image.copy()
        
        if ids is not None:
            # Draw detected markers
            cv2.aruco.drawDetectedMarkers(annotated_image, corners, ids)
            
            # Calculate centers
            for i, marker_id in enumerate(ids.flatten()):
                if marker_id in range(8):  # Only use markers 0-7
                    corner = corners[i][0]
                    center_x = int(np.mean(corner[:, 0]))
                    center_y = int(np.mean(corner[:, 1]))
                    marker_centers[marker_id] = (center_x, center_y)
                    
                    # Draw center point
                    cv2.circle(annotated_image, (center_x, center_y), 5, (0, 255, 0), -1)
                    cv2.putText(annotated_image, f"ID{marker_id}", 
                              (center_x + 10, center_y), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.6, (0, 255, 0), 2)
        
        return marker_centers, annotated_image
    
    def calculate_pixel_to_mm_ratio(self, marker_centers: Dict) -> Tuple[float, Dict]:
        """
        Calculate pixel to mm ratio using ArUco markers - EXACT V12
        
        Args:
            marker_centers: Dictionary of marker centers
            
        Returns:
            Tuple of (average_ratio, individual_ratios)
        """
        ratios = []
        individual_ratios = {}
        
        for (id1, id2), expected_distance in self.reference_distances.items():
            if id1 in marker_centers and id2 in marker_centers:
                center1 = marker_centers[id1]
                center2 = marker_centers[id2]
                
                # Calculate pixel distance
                pixel_distance = np.sqrt((center1[0] - center2[0])**2 + 
                                       (center1[1] - center2[1])**2)
                
                # Calculate ratio
                ratio = expected_distance / pixel_distance
                ratios.append(ratio)
                individual_ratios[f"{id1}-{id2}"] = {
                    'pixel_distance': pixel_distance,
                    'expected_mm': expected_distance,
                    'ratio': ratio
                }
        
        if not ratios:
            raise ValueError("Not enough ArUco markers detected for calibration")
        
        average_ratio = np.mean(ratios)  # EXACT V12
        
        return average_ratio, individual_ratios
    
    
    def preprocess_for_sandal_detection(self, image: np.ndarray, marker_centers: Dict = None) -> Tuple[np.ndarray, Dict]:
        """
        Optimized preprocessing with enhanced method combination and weighted scoring
        """
        # Convert to different color spaces
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # OPTIMIZATION 1: Dynamic parameter adjustment based on image characteristics
        img_height, img_width = gray.shape
        img_area = img_height * img_width
        img_diagonal = np.sqrt(img_height**2 + img_width**2)
        
        # Analyze image brightness and contrast for adaptive parameters
        mean_brightness = np.mean(gray)
        contrast = np.std(gray)
        
        # Adaptive preprocessing parameters
        blur_kernel = 7 if contrast > 30 else 5
        blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        
        preprocessing_results = {}
        
        # OPTIMIZATION 2: Enhanced Method 1 - Adaptive Thresholding with dynamic parameters
        block_size = max(11, int(img_diagonal / 100))  # Dynamic block size
        if block_size % 2 == 0:
            block_size += 1
        
        adaptive1 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY_INV, block_size, 3)
        adaptive2 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                        cv2.THRESH_BINARY_INV, block_size + 4, 5)
        
        # OPTIMIZATION 3: Method 2 - Enhanced Otsu with preprocessing
        # Apply CLAHE for better contrast before Otsu
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced_gray = clahe.apply(gray)
        blurred_enhanced = cv2.GaussianBlur(enhanced_gray, (5, 5), 0)
        _, otsu = cv2.threshold(blurred_enhanced, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # OPTIMIZATION 4: Method 3 - Dynamic dark threshold based on image brightness
        dark_threshold = max(60, min(120, int(mean_brightness * 0.7)))
        dark_mask = cv2.inRange(gray, 0, dark_threshold)
        
        # OPTIMIZATION 5: Method 4 - Multi-range HSV segmentation
        # Primary range for very dark objects
        lower_dark1 = np.array([0, 0, 0])
        upper_dark1 = np.array([180, 255, 80])
        hsv_mask1 = cv2.inRange(hsv, lower_dark1, upper_dark1)
        
        # Secondary range for medium-dark objects
        lower_dark2 = np.array([0, 0, 81])
        upper_dark2 = np.array([180, 100, 130])
        hsv_mask2 = cv2.inRange(hsv, lower_dark2, upper_dark2)
        
        hsv_mask = cv2.bitwise_or(hsv_mask1, hsv_mask2)
        
        # OPTIMIZATION 6: Method 5 - Enhanced LAB processing
        l_channel = lab[:, :, 0]
        # Apply median filter to reduce noise before thresholding
        l_filtered = cv2.medianBlur(l_channel, 5)
        _, lab_binary = cv2.threshold(l_filtered, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # NEW METHOD 6: Edge-based detection for clear boundaries
        edges = cv2.Canny(blurred, 50, 150)
        # Dilate edges to create regions
        kernel_edge = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        edge_mask = cv2.dilate(edges, kernel_edge, iterations=2)
        
        # NEW METHOD 7: Gradient-based detection
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        magnitude = np.uint8(255 * magnitude / np.max(magnitude))
        _, gradient_mask = cv2.threshold(magnitude, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # OPTIMIZATION 7: Weighted combination instead of simple OR
        combined = self.weighted_combination([
            (adaptive1, 0.25),
            (otsu, 0.25),
            (dark_mask, 0.20),
            (hsv_mask, 0.15),
            (lab_binary, 0.10),
            (edge_mask, 0.05)
        ])
        
        preprocessing_results = {
            'adaptive_gaussian': adaptive1,
            'adaptive_mean': adaptive2,
            'otsu_enhanced': otsu,
            'dark_mask_dynamic': dark_mask,
            'hsv_mask_multi': hsv_mask,
            'lab_enhanced': lab_binary,
            'edge_based': edge_mask,
            'gradient_based': gradient_mask,
            'weighted_combined': combined
        }
        
        # Apply ArUco protection with adaptive radius
        if marker_centers:
            exclusion_radius = max(20, int(img_diagonal / 60))  # Smaller, more precise
            aruco_mask = np.zeros_like(gray)
            for center in marker_centers.values():
                cv2.circle(aruco_mask, center, exclusion_radius, 255, -1)
            
            for name, binary_img in preprocessing_results.items():
                preprocessing_results[name] = cv2.bitwise_and(binary_img, cv2.bitwise_not(aruco_mask))
        
        # OPTIMIZATION 8: Adaptive morphological operations
        processed_results = self.adaptive_morphology(preprocessing_results, img_diagonal, marker_centers)
        
        # Enhanced selection with multiple criteria
        best_binary, best_method = self.enhanced_selection(processed_results, image, marker_centers)
        
        return best_binary, {
            'method_used': best_method,
            'all_methods': processed_results,
            'preprocessing_info': preprocessing_results,
            'image_stats': {
                'brightness': mean_brightness,
                'contrast': contrast,
                'size': img_area
            }
        }
    
    def weighted_combination(self, method_weights: List[Tuple[np.ndarray, float]]) -> np.ndarray:
        """
        Create weighted combination of binary images
        """
        if not method_weights:
            return np.zeros((100, 100), dtype=np.uint8)
        
        height, width = method_weights[0][0].shape
        combined = np.zeros((height, width), dtype=np.float32)
        
        for binary_img, weight in method_weights:
            combined += (binary_img.astype(np.float32) / 255.0) * weight
        
        # Threshold the weighted result
        _, result = cv2.threshold((combined * 255).astype(np.uint8), 127, 255, cv2.THRESH_BINARY)
        return result
    
    def adaptive_morphology(self, preprocessing_results: Dict, img_diagonal: float, marker_centers: Dict = None) -> Dict:
        """
        Apply adaptive morphological operations based on image and marker characteristics
        """
        # Base kernel sizes
        base_small = max(3, int(img_diagonal / 300))
        base_medium = max(5, int(img_diagonal / 150))
        base_large = max(7, int(img_diagonal / 100))
        
        # Adjust for marker proximity
        if marker_centers and len(marker_centers) >= 4:
            marker_positions = list(marker_centers.values())
            min_distance = self.calculate_min_marker_distance(marker_positions)
            
            if min_distance < img_diagonal * 0.15:
                base_medium = max(3, base_medium // 2)
                base_large = max(5, base_large // 2)
        
        # Ensure odd kernel sizes
        kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                               (base_small + (base_small % 2 - 1), base_small + (base_small % 2 - 1)))
        kernel_medium = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                                (base_medium + (base_medium % 2 - 1), base_medium + (base_medium % 2 - 1)))
        kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                               (base_large + (base_large % 2 - 1), base_large + (base_large % 2 - 1)))
        
        processed_results = {}
        for name, binary_img in preprocessing_results.items():
            # Multi-stage morphological processing
            # Stage 1: Close small gaps
            closed = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel_small)
            
            # Stage 2: Remove small noise
            opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_small)
            
            # Stage 3: Fill medium gaps
            closed2 = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_medium)
            
            # Stage 4: Final smoothing for sandal shape
            final = cv2.morphologyEx(closed2, cv2.MORPH_CLOSE, kernel_large)
            
            processed_results[name] = final
        
        return processed_results
    
    def calculate_min_marker_distance(self, marker_positions: List) -> float:
        """Calculate minimum distance between any two markers"""
        min_distance = float('inf')
        for i in range(len(marker_positions)):
            for j in range(i+1, len(marker_positions)):
                dist = np.sqrt((marker_positions[i][0] - marker_positions[j][0])**2 + 
                             (marker_positions[i][1] - marker_positions[j][1])**2)
                min_distance = min(min_distance, dist)
        return min_distance
    
    def enhanced_selection(self, processed_results: Dict, original_image: np.ndarray, marker_centers: Dict = None) -> Tuple[np.ndarray, str]:
        """
        Enhanced selection with multiple scoring criteria and confidence levels
        """
        best_score = 0
        best_binary = None
        best_method = "weighted_combined"
        
        image_area = original_image.shape[0] * original_image.shape[1]
        
        # Method priority weights (some methods are inherently more reliable)
        method_weights = {
            'weighted_combined': 1.2,
            'otsu_enhanced': 1.1,
            'adaptive_gaussian': 1.0,
            'hsv_mask_multi': 0.9,
            'dark_mask_dynamic': 0.8,
            'lab_enhanced': 0.7,
            'edge_based': 0.6,
            'gradient_based': 0.5
        }
        
        for method_name, binary_img in processed_results.items():
            try:
                contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if not contours:
                    continue
                
                # Get largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)
                
                # Enhanced area filtering
                if contour_area < image_area * 0.005 or contour_area > image_area * 0.85:
                    continue
                
                # ArUco overlap check
                if marker_centers and self.contour_overlaps_markers(largest_contour, marker_centers):
                    continue
                
                # Calculate enhanced metrics
                score = self.calculate_enhanced_score(largest_contour, image_area)
                
                # Apply method weight
                weighted_score = score * method_weights.get(method_name, 1.0)
                
                if weighted_score > best_score:
                    best_score = weighted_score
                    best_binary = binary_img
                    best_method = method_name
                    
            except Exception as e:
                print(f"Error evaluating method {method_name}: {e}")
                continue
        
        # Enhanced fallback strategy
        if best_binary is None:
            fallback_order = ['weighted_combined', 'otsu_enhanced', 'adaptive_gaussian']
            for method in fallback_order:
                if method in processed_results:
                    best_binary = processed_results[method]
                    best_method = f'{method}_fallback'
                    break
        
        print(f"🎯 Best method: {best_method} (score: {best_score:.2f})")
        return best_binary, best_method
    
    def contour_overlaps_markers(self, contour: np.ndarray, marker_centers: Dict) -> bool:
        """Check if contour overlaps with any ArUco markers"""
        for marker_center in marker_centers.values():
            if cv2.pointPolygonTest(contour, marker_center, False) >= 0:
                return True
        return False
    
    def calculate_enhanced_score(self, contour: np.ndarray, image_area: float) -> float:
        """
        Enhanced scoring system with more comprehensive metrics
        """
        contour_area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return 0
        
        # Basic metrics
        circularity = 4 * np.pi * contour_area / (perimeter * perimeter)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else 0
        extent = contour_area / (w * h) if (w * h) > 0 else 0
        
        # Advanced metrics
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = contour_area / hull_area if hull_area > 0 else 0
        
        # Contour smoothness
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        smoothness = len(approx)
        
        # Enhanced scoring
        score = 0
        
        # Size score (optimized for sandals)
        size_ratio = contour_area / image_area
        if 0.03 <= size_ratio <= 0.4:
            score += 35
        elif 0.01 <= size_ratio <= 0.6:
            score += 25
        
        # Aspect ratio (sandals are typically elongated)
        if 1.8 <= aspect_ratio <= 3.5:
            score += 30
        elif 1.3 <= aspect_ratio <= 4.5:
            score += 20
        
        # Extent (how well contour fills bounding box)
        if 0.4 <= extent <= 0.8:
            score += 25
        elif 0.25 <= extent <= 0.9:
            score += 15
        
        # Solidity (convexity measure)
        if 0.6 <= solidity <= 0.95:
            score += 20
        elif 0.4 <= solidity <= 0.98:
            score += 10
        
        # Circularity (sandals should not be too circular)
        if 0.15 <= circularity <= 0.5:
            score += 15
        elif 0.08 <= circularity <= 0.7:
            score += 8
        
        # Smoothness bonus
        if 8 <= smoothness <= 20:
            score += 15
        elif 6 <= smoothness <= 25:
            score += 10
        
        return score
    
    def detect_sandal_contour(self, binary_image: np.ndarray, original_image: np.ndarray, preprocessing_info: Dict, marker_centers: Dict = None) -> Tuple[np.ndarray, np.ndarray, Dict]:
        """
        Enhanced sandal contour detection with multiple validation methods - EXACT V12 + ArUco protection
        
        Args:
            binary_image: Preprocessed binary image
            original_image: Original color image for visualization
            preprocessing_info: Information from preprocessing step
            marker_centers: Dictionary of ArUco centers for protection
            
        Returns:
            Tuple of (refined_contour, annotated_image, contour_info)
        """
        # Find all contours - EXACT V12
        contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            raise ValueError("No contours found in the image")
        
        # Advanced contour filtering and selection - EXACT V12
        valid_contours = []
        image_area = original_image.shape[0] * original_image.shape[1]
        
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            
            # Filter by area (sandal should be significant portion of image) - EXACT V12
            if area < image_area * 0.005:  # Too small
                continue
            if area > image_area * 0.8:    # Too large (likely background)
                continue
                
            # Filter by contour properties - EXACT V12
            perimeter = cv2.arcLength(contour, True)
            if perimeter < 100:  # Too small perimeter
                continue
                
            # Check aspect ratio - EXACT V12
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else 0
            
            if aspect_ratio > 10:  # Too elongated (likely noise)
                continue
            
            # ADDITION: Check if contour overlaps with ArUco markers
            if marker_centers:
                overlaps_aruco = False
                for marker_center in marker_centers.values():
                    if cv2.pointPolygonTest(contour, marker_center, False) >= 0:
                        overlaps_aruco = True
                        break
                
                if overlaps_aruco:
                    continue  # Skip contours that contain ArUco markers
                
            valid_contours.append({
                'contour': contour,
                'area': area,
                'perimeter': perimeter,
                'aspect_ratio': aspect_ratio,
                'bounding_rect': (x, y, w, h)
            })
        
        if not valid_contours:
            raise ValueError("No valid sandal contours found")
        
        # Select best contour (largest valid one) - EXACT V12
        best_contour_info = max(valid_contours, key=lambda x: x['area'])
        largest_contour = best_contour_info['contour']
        
        # Refine contour using multiple techniques - EXACT V12
        refined_contour = self.refine_sandal_contour(largest_contour, binary_image, original_image)
        
        # Create detailed annotated image - EXACT V12
        annotated_image = original_image.copy()
        
        # Draw original contour in blue
        cv2.drawContours(annotated_image, [largest_contour], -1, (255, 0, 0), 2)
        
        # Draw refined contour in cyan
        cv2.drawContours(annotated_image, [refined_contour], -1, (0, 255, 255), 3)
        
        # Draw bounding rectangle
        x, y, w, h = cv2.boundingRect(refined_contour)
        cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Draw convex hull for comparison
        hull = cv2.convexHull(refined_contour)
        cv2.drawContours(annotated_image, [hull], -1, (255, 255, 0), 1)
        
        # Add contour information text - EXACT V12
        contour_info = {
            'original_contour': largest_contour,
            'refined_contour': refined_contour,
            'convex_hull': hull,
            'area': cv2.contourArea(refined_contour),
            'perimeter': cv2.arcLength(refined_contour, True),
            'bounding_rect': (x, y, w, h),
            'contour_count': len(contours),
            'valid_contour_count': len(valid_contours),
            'preprocessing_method': preprocessing_info.get('method_used', 'unknown')
        }
        
        
        return refined_contour, annotated_image, contour_info
    
    def refine_sandal_contour(self, contour: np.ndarray, binary_image: np.ndarray, original_image: np.ndarray) -> np.ndarray:
        """
        Refine sandal contour to better capture the complete sandal shape - EXACT V12
        
        Args:
            contour: Initial contour
            binary_image: Binary image
            original_image: Original image
            
        Returns:
            Refined contour
        """
        try:
            # Method 1: Convex hull approach (for sandals with concave parts) - EXACT V12
            hull = cv2.convexHull(contour)
            
            # Method 2: Contour approximation with different epsilon values - EXACT V12
            perimeter = cv2.arcLength(contour, True)
            
            # Try different approximation levels - EXACT V12
            approx_tight = cv2.approxPolyDP(contour, 0.005 * perimeter, True)
            approx_medium = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            approx_loose = cv2.approxPolyDP(contour, 0.05 * perimeter, True)
            
            # Method 3: Morphological operations on contour region - EXACT V12
            # Create mask from contour
            mask = np.zeros(binary_image.shape, dtype=np.uint8)
            cv2.fillPoly(mask, [contour], 255)
            
            # Dilate to capture missing parts - EXACT V12
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
            dilated_mask = cv2.dilate(mask, kernel, iterations=2)
            
            # Find contour of dilated mask - EXACT V12
            dilated_contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if dilated_contours:
                dilated_contour = max(dilated_contours, key=cv2.contourArea)
            else:
                dilated_contour = contour
            
            # Method 4: Minimum area rectangle approach - EXACT V12
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            # Evaluate which refined contour is best - EXACT V12
            candidates = {
                'original': contour,
                'hull': hull,
                'approx_tight': approx_tight,
                'approx_medium': approx_medium,
                'dilated': dilated_contour,
                'min_rect': box.reshape(-1, 1, 2)
            }
            
            # Score each candidate - EXACT V12
            best_contour = contour
            best_score = 0
            
            original_area = cv2.contourArea(contour)
            
            for name, candidate in candidates.items():
                try:
                    area = cv2.contourArea(candidate)
                    
                    # Skip if area is too different from original - EXACT V12
                    area_ratio = area / original_area if original_area > 0 else 0
                    if area_ratio < 0.8 or area_ratio > 2.0:
                        continue
                    
                    # Calculate shape quality metrics - EXACT V12
                    perimeter = cv2.arcLength(candidate, True)
                    
                    if perimeter == 0:
                        continue
                    
                    # Prefer contours that are larger but not too much larger - EXACT V12
                    score = 0
                    
                    # Area score - EXACT V12
                    if 1.0 <= area_ratio <= 1.3:  # 0-30% larger is good
                        score += 40
                    elif 0.9 <= area_ratio <= 1.5:
                        score += 20
                    
                    # Smoothness score (fewer vertices for similar area is better) - EXACT V12
                    if name in ['hull', 'approx_medium', 'min_rect']:
                        score += 15
                    
                    # Shape completeness (dilated version might capture missing parts) - EXACT V12
                    if name == 'dilated' and area_ratio > 1.1:
                        score += 25
                    
                    if score > best_score:
                        best_score = score
                        best_contour = candidate
                        
                except Exception as e:
                    continue
            
            return best_contour
            
        except Exception as e:
            print(f"Error in contour refinement: {e}")
            return contour
    
    def calculate_sandal_dimensions(self, contour: np.ndarray, pixel_to_mm_ratio: float) -> Dict:
        """
        Calculate sandal dimensions from contour - EXACT V12
        
        Args:
            contour: Sandal contour
            pixel_to_mm_ratio: Calibrated pixel to mm ratio
            
        Returns:
            Dictionary containing dimension measurements
        """
        # Get bounding rectangle - EXACT V12
        x, y, w, h = cv2.boundingRect(contour)
        
        # Get minimum area rectangle (oriented bounding box) - EXACT V12
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        # Calculate dimensions from minimum area rectangle - EXACT V12
        width_pixels = rect[1][0]  # Width in pixels
        height_pixels = rect[1][1]  # Height in pixels
        
        # Ensure length > width convention - EXACT V12
        if width_pixels > height_pixels:
            length_pixels = width_pixels
            width_pixels = height_pixels
        else:
            length_pixels = height_pixels
        
        # Convert to mm - EXACT V12
        raw_length_mm = length_pixels * pixel_to_mm_ratio
        raw_width_mm = width_pixels * pixel_to_mm_ratio
        
        # Calculate area - EXACT V12
        contour_area_pixels = cv2.contourArea(contour)
        area_mm2 = contour_area_pixels * (pixel_to_mm_ratio ** 2)
        
        # Calculate perimeter - EXACT V12
        perimeter_pixels = cv2.arcLength(contour, True)
        perimeter_mm = perimeter_pixels * pixel_to_mm_ratio
        
        return {
            'raw_length_mm': raw_length_mm,
            'raw_width_mm': raw_width_mm,
            'area_mm2': area_mm2,
            'perimeter_mm': perimeter_mm,
            'bounding_rect': (x, y, w, h),
            'oriented_box': box,
            'length_pixels': length_pixels,
            'width_pixels': width_pixels,
            'angle': rect[2]
        }
    
    def adaptive_error_correction(self, raw_measurements: Dict) -> Dict:
        """
        Apply simple fixed error correction - optimized for accuracy
        """
        length_mm = raw_measurements['raw_length_mm']
        width_mm = raw_measurements['raw_width_mm']
        corrected_measurements = raw_measurements.copy()
         
        # Koreksi yang lebih presisi
        # Jika hasil saat ini 3-5mm lebih kecil, berarti perlu koreksi lebih kecil
        length_correction = 0.947  # Lebih kecil dari 0.94, mengurangi koreksi berlebihan
        width_correction = 0.947
        
        corrected_measurements['corrected_length_mm'] = length_mm * length_correction
        corrected_measurements['corrected_width_mm'] = width_mm * width_correction
        corrected_measurements['length_correction_factor'] = length_correction
        corrected_measurements['width_correction_factor'] = width_correction
        
        return corrected_measurements
    def process_image(self, image: np.ndarray) -> Tuple[Dict, np.ndarray]:
        """
        Process a single image to measure sandal dimensions - EXACT V12 + ArUco Protection
        
        Args:
            image: Input image
            show_steps: Whether to show intermediate processing steps
            
        Returns:
            Tuple of (measurements, result_image)
        """
        try:
            # Step 1: Detect ArUco markers - EXACT V12
            marker_centers, marked_image = self.detect_aruco_markers(image)
            
            if len(marker_centers) < 3:
                raise ValueError(f"Insufficient ArUco markers detected: {len(marker_centers)}/8")
                
            # Step 2: Calculate pixel-to-mm ratio - EXACT V12
            pixel_to_mm_ratio, calibration_details = self.calculate_pixel_to_mm_ratio(marker_centers)
                
            # Step 3: Advanced preprocessing for sandal detection - EXACT V12 + ArUco Protection
            binary_image, preprocessing_info = self.preprocess_for_sandal_detection(image, marker_centers)
                
            # Step 4: Enhanced sandal contour detection - EXACT V12 + ArUco Protection
            sandal_contour, contour_image, contour_info = self.detect_sandal_contour(binary_image, marked_image, preprocessing_info, marker_centers)
                
            # Step 5: Calculate raw dimensions - EXACT V12
            raw_measurements = self.calculate_sandal_dimensions(sandal_contour, pixel_to_mm_ratio)
                
            # Step 6: Apply adaptive error correction - EXACT V12
            final_measurements = self.adaptive_error_correction(raw_measurements)
                
            # Add preprocessing and contour information - EXACT V12
            final_measurements['preprocessing_info'] = preprocessing_info
            final_measurements['contour_info'] = contour_info
            final_measurements['pixel_to_mm_ratio'] = pixel_to_mm_ratio
            final_measurements['calibration_details'] = calibration_details
            final_measurements['markers_detected'] = len(marker_centers)
                
            # Create final result image - EXACT V12
            result_image = contour_image.copy()
                
            # Draw oriented bounding box - EXACT V12
            cv2.drawContours(result_image, [final_measurements['oriented_box']], -1, (255, 0, 0), 2)          
            return final_measurements, result_image
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return {}, image
