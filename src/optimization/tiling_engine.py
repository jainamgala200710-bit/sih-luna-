import numpy as np

class TilingEngine:
    """
    Splits massive ISRO satellite arrays into manageable structural blocks to 
    prevent memory exhaustion during dense SIFT extraction or Deep Learning inference.
    """
    
    @staticmethod
    def extract_tiles(image: np.ndarray, tile_size: int = 1000, overlap: int = 100):
        """
        Generates overlapping tiles from a large image.
        Returns a list of (tile, (start_y, start_x)) tuples.
        """
        h, w = image.shape[:2]
        tiles = []
        
        stride = tile_size - overlap
        if stride <= 0:
            raise ValueError("Overlap must be strictly less than tile_size")
            
        for y in range(0, h, stride):
            for x in range(0, w, stride):
                # Ensure we don't go out of bounds
                end_y = min(y + tile_size, h)
                end_x = min(x + tile_size, w)
                
                # Adjust start to keep tiles consistent size if possible, 
                # though at edges they might be smaller.
                start_y = max(0, end_y - tile_size) if y + tile_size > h else y
                start_x = max(0, end_x - tile_size) if x + tile_size > w else x
                
                tile = image[start_y:end_y, start_x:end_x]
                tiles.append((tile, (start_y, start_x)))
                
                if end_x == w:
                    break
            if end_y == h:
                break
                
        return tiles

    @staticmethod
    def adjust_keypoint_coordinates(keypoints, offset_y: int, offset_x: int):
        """
        Remaps localized tile keypoints back into the global coordinate space of the master image.
        """
        for kp in keypoints:
            x, y = kp.pt
            kp.pt = (x + offset_x, y + offset_y)
        return keypoints
