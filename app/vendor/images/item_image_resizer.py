from PIL import Image
import os

# creates another image used as thumbnail thats 300X 300
basewidth_225 = 225
basewidth_500 = 500
extension = ".jpg"


ext = ['.jpg', '.png', '.gif', '.png', '.jpeg']


def testsize(pathofimage):
    with Image.open(pathofimage) as img:
        width, height = img.size
        if width == 250:
            return 1
        else:
            return 0

def convertimage(thefile, pathoffile, directoryofimage):
    print("File format incorrect ...")
    filename, exti = os.path.splitext(thefile)
    img = Image.open(pathoffile)
    im = img.convert('RGB')
    extoffile = (directoryofimage + "/")
    oldfile = extoffile + thefile
    im.save((extoffile + filename + ".jpg"), quality=95)
    if not thefile.endswith(".jpg"):
        os.remove(oldfile)


def convertimage_225(newfullpathfilename, root, file):
    # CREATE A 250 size image
    # opens the image
    img = Image.open(newfullpathfilename)
    # gets base name
    thebasename = os.path.splitext(file)[0]
    newname_225 = thebasename + "_225x"
    renamed_file = (os.path.join(root, newname_225 + extension))
    # test to see if already done
    seeifexists = os.path.exists(renamed_file)
    if seeifexists is True:
        print("IMAGE EXISTS!")
    else:
        # creates new basename
        print("")
        print("*"*10)
        print("name: ", newfullpathfilename)
        print("format:", img.format)
        print("dimensions:",  "%dx%d" % img.size)
        # convert
        wpercent = (basewidth_225/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth_225, hsize), Image.ANTIALIAS)
        imagesave = os.path.join(root, renamed_file)
        img.save(imagesave, subsampling=0, quality=100, optimize=True)
        os.chmod(renamed_file, 0o775)
        print("converted")
        print("name: ", renamed_file)
        print("dimensions:", "%dx%d" % img.size)
        print("*"*10)
        print("")
        getsize = os.path.getsize(imagesave)
        if getsize == 0:
            os.remove(imagesave)


def convertimage_500(newfullpathfilename, root, file):
    # CREATE A 250 size image
    # opens the image
    img = Image.open(newfullpathfilename)
    # gets base name
    thebasename = os.path.splitext(file)[0]
    newname_500 = thebasename + "_500x"
    renamed_file = (os.path.join(root, newname_500 + extension))
    # test to see if already done
    seeifexists = os.path.exists(renamed_file)
    if seeifexists is True:
        print("IMAGE EXISTS!")
    else:
        # creates new basename
        print("")
        print("*"*10)
        print("name: ", newfullpathfilename)
        print("format:", img.format)
        print("dimensions:",  "%dx%d" % img.size)
        # convert
        wpercent = (basewidth_500/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth_500, hsize), Image.ANTIALIAS)
        imagesave = os.path.join(root, renamed_file)
        img.save(imagesave, subsampling=0, quality=100, optimize=True)
        os.chmod(renamed_file, 0o775)
        print("converted")
        print("name: ", renamed_file)
        print("dimensions:", "%dx%d" % img.size)
        print("*"*10)
        print("")
        # if size is 0 delete it
        getsize = os.path.getsize(imagesave)
        if getsize == 0:
            os.remove(imagesave)


def imagespider(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(tuple(ext)):
                # path of image and file
                pathofimage = (os.path.join(root, file))
                # get file name with extension
                filename_w_ext = os.path.basename(pathofimage)
                # split file name and extension
                filename, file_extension = os.path.splitext(filename_w_ext)
                # get root directory name and extension
                newfullpathfilename = root + '/' + filename + extension

                # convert image if not jpg
                if not file.endswith(".jpg"):
                    convertimage(
                        thefile=file, pathoffile=pathofimage, directoryofimage=root)
                # pass files already dne
                if file.endswith("_225x.jpg"):
                    pass
                elif file.endswith("_500x.jpg"):
                    pass
                else:
                    # see if width greater than 250
                    y = testsize(newfullpathfilename)
                    if y == 1:
                        pass
                    else:
                        # convert image to 225
                        convertimage_225(newfullpathfilename, root, file)
                        # convert image to 500
                        convertimage_500(newfullpathfilename, root, file)
