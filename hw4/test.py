from PIL import Image

im = Image.open('homework4.png')

pix_val=list(im.getdata())
pix_flat=[x for sets in pix_val for x in sets]

data = ""
for i in range(0,len(pix_flat),3):
    for j in range(3):
        print i,j
        data += "0" if pix_flat[i+j]%2==0 else "1"

print data

