# convert a binary image into ASCII
import cv2

img = cv2.imread('world_map.png', cv2.IMREAD_REDUCED_GRAYSCALE_2)
width, height = 200, 50
res = cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_AREA)
threshold = 229
_, bw_img = cv2.threshold(res, threshold, 1, cv2.THRESH_BINARY)
cv2.imwrite('world_map.jpg', bw_img)

file_object = open(r'world_map.txt', 'w+')
world_map = []

for i in range(height):
    for j in range(width):
        if bw_img[i][j] == 1:
            world_map.append('*')
        else:
            world_map.append(' ')
    world_map.append('\n')
file_object.write('|'.join(world_map))
# print(''.join(world_map))
file_object.close()

print('Done!')