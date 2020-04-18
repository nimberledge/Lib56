from PIL import Image

def split_cards(filename):
    im = Image.open(filename)
    # print ("Image size: {}".format(im.size))
    x, y = im.size
    # im.show()
    card_x = x // 13
    card_y = y // 5
    card_labels = 'A23456789TJQK'
    card_suits = 'CDHS'
    card_to_image_map = {}
    guess_delta = 3
    guess_step = 1
    for i in range(len(card_labels)):
        for j in range(len(card_suits)):

            card_name = card_labels[i] + card_suits[j]
            top_left = (i * card_x, j*card_y)
            bottom_right = ((i+1) * card_x, (j+1) * card_y)


            if i >= 8:
                image = im.crop(box=(i*card_x+guess_delta, j*card_y, (i+1)*card_x + guess_delta, (j+1)*card_y))
                if i == 11:
                    guess_step = 0
                else:
                    guess_delta += guess_step
                    guess_step = 0.5

            else:
                image = im.crop(box=(i*card_x, j*card_y, (i+1)*card_x, (j+1)*card_y))
            card_to_image_map[card_name] = image
    card_to_image_map['face-down'] = im.crop(box=(2*card_x, 4*card_y, 3*card_x, 5*card_y))
    for card in card_to_image_map.keys():
        print ("Saving file {}.png".format(card))
        try:
            card_to_image_map[card].save('individual_card_png/'+card+'.png')
        except:
            print ("Error saving card {}, terminating".format(card))
            break
    else:
        print ("Saved all cards successfully")

def test_main():
    filename = 'cards.png'
    split_cards(filename)

if __name__ == '__main__':
    test_main()
