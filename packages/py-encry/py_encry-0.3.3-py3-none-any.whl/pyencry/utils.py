import random #seed, randint

def get_pixels(width, height):
    for n in range(width):
        for m in range(height):
            yield (n, m)

def encode_data_to_pixel(pixel, data):
    new_pixel = [0, 0, 0, 0]

    data = bin(data)

    i = 0
    while i <= 3:
        channel = pixel[i]

        # Konverterar data till binärt i en sträng med korrekt antal siffror (8) 
        binary_data = f"0b{"0" * (10 - len(data))}{data[2:]}"
        
        # Plockar ut delen av datan att sätta i varje pixel
        subdata = int((binary_data)[2*i+2 : 2*i+4], 2)

        # Sätter in data
        channel = channel >> 2 << 2 
        channel += subdata
        
        new_pixel[i] = channel

        i += 1

    return tuple(new_pixel)


def decode_data_from_pixel(pixel):
    data = "0b"

    for channel in pixel:

        if len(bin(channel)) < 4:
            binary_data = f"0b0{bin(channel)[-1]}"
        else:
            binary_data = bin(channel)

        data += binary_data[-2:]

    data = int(data, 2)
    return data

  
def get_rail_fence_pixels(width, height, rail_fence_height):
    h = 0
    w = 0
    rail = 0
    down = True
    while w < width:
        if down:
            h += 1
            rail += 1
        else:
            h -= 1
            rail -= 1
        if rail % (rail_fence_height - 1) == 0 :
            down = not down
        yield (w, h)
        w += 1
        if w + 1 == width:
            w = 0
            h += rail_fence_height
        if h + 1 == height:
            break


def get_random_spacing_pixels(height, width, key):
    random.seed(key)
    i = 0
    while i < height:
        j = 0
        while j < width:
            j += random.randint(1,5)
            if j >= width:
                break
            yield(i, j)
        i += 1
