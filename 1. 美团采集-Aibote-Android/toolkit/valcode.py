import ddddocr


class dOcr:
    def __init__(self):
        self.ocr = ddddocr.DdddOcr()
        print("初始化完成...")

    def predict(self, imagePath):
        with open(imagePath, 'rb') as f:
            img_bytes = f.read()
        valCode = self.ocr.classification(img_bytes)
        return valCode


ocr = dOcr()
if __name__ == "__main__":
    temp = dOcr()
    temp.predict('./data/验证码')
