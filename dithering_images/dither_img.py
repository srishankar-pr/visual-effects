#this is the script to dither image
import cv2 as cv
import numpy as np 


INPUT_FILE="f40 5.jpg"
OUTPUT_FILE="out_67.jpg"
RESIZE=None


#declaring the bayer matrix 


BAYER=np.array([
    [0,8,2,10],
    [12,4,14,6],
    [3,11,1,9],
    [15,7,13,5]
],dtype=np.uint8)



#extracting thresholds from dithering 
def ordered_dither(img,bayer):

    # ONLY convert to grayscale if image has 3 channels
    if len(img.shape) > 2:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    height, width = img.shape
    N = bayer.shape[0]


    #tiling the bayer matrix over the complete image 
    tiled = np.tile(bayer, (height//N + 1, width//N + 1))

    #cut to match image size
    tiled = tiled[:height, :width].astype(np.float32)

    #obtaining per-pixel thresholds
    threshold_map = (tiled + 0.5) / (N*N) * 255.0

    #perform dithering using numpy comparison
    output = (img > threshold_map).astype(np.uint8) * 255

    return output


def main():
    print(f"loading image {INPUT_FILE}...")
    img = cv.imread(INPUT_FILE)   # Load normally now (color)

    if img is None:
        print("Error in loading image try again")
        return

    dithered = ordered_dither(img, BAYER)
    cv.imwrite(OUTPUT_FILE, dithered)
    print(f"Dithering done saved as {OUTPUT_FILE}")

    cv.imshow("dithered output", dithered)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__=="__main__":
   main()
