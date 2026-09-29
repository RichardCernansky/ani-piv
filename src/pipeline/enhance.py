import cv2
import numpy as np
from collections import deque

def enhance_img():
    
    return


class Pixel:
   def __init__(self, row, col):
       self.row = row
       self.col = col

def image_reconstruct(marker: np.ndarray, mask: np.ndarray) -> np.ndarray:
   """
   Perform morphological reconstruction by dilation.

   Parameters:
       marker (np.ndarray): The marker image (seed), eroded inverted input.
       mask (np.ndarray): The mask image (constraint), inverted input.

   Returns:
       np.ndarray: Reconstructed image.
   """
   if marker.shape != mask.shape:
       raise ValueError("Marker and mask must have the same dimensions")

   # Ensure images are in the same type
   marker = marker.astype(mask.dtype)

   # Create a working copy
   reconstructed = marker.copy()

   # Use a queue for pixels to update
   q = deque()
   rows, cols = reconstructed.shape

   # Initialize queue with pixels where marker < mask
   for r in range(rows):
       for c in range(cols):
           if reconstructed[r, c] < mask[r, c]:
               q.append(Pixel(r, c))

   # Neighbor offsets (4-connectivity)
   neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

   while q:
       p = q.popleft()
       for dr, dc in neighbors:
           rr, cc = p.row + dr, p.col + dc
           if 0 <= rr < rows and 0 <= cc < cols:

               new_val = min(mask[rr, cc], max(reconstructed[rr, cc], reconstructed[p.row, p.col])) # 1. max - set the neighbor pixel according to the current pixel value, 2. min - make sure it does not exceed the mask value
               if new_val > reconstructed[rr, cc]:
                   reconstructed[rr, cc] = new_val
                   q.append(Pixel(rr, cc))

   return reconstructed

def morphological_reconstruction(base: np.ndarray, e: dict) -> np.ndarray:
    # invert
    inv = 255 - base  
    # erode the inverted image to create a marker
    marker = cv2.erode(inv, np.ones((e["erode_size"], e["erode_size"]), np.uint8), iterations=1)
    # reconstruct
    reconstructed = image_reconstruct(marker, inv)


    return reconstructed
