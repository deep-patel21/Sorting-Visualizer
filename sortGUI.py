import pygame
import math
import random
pygame.init()

class drawInformation:
    black = 0, 0, 0
    white = 255, 255, 255
    red = 255, 0, 0 
    green = 0, 255, 0
    blue = 0, 0, 255
    cyan = 0, 255, 255
    darkblue = 0, 0, 139
    lightblue = 108, 159, 206
    backgroundColor = white
    gradientColor = [cyan, lightblue, darkblue]
    fontOne = pygame.font.SysFont('comfortaa', 30)
    fontTwo = pygame.font.SysFont('comfortaa', 40)
    sidePadding = 0
    topPadding = 200
    def __init__(self, width, height, array):
        self.width = width
        self.height = height
        pygame.display.set_caption("Sorting Algorithm Visualizer - Deep Patel")
        self.window = pygame.display.set_mode((width, height))
        self.setArray(array)
    def setArray(self, array):
        self.array = array
        self.minimum = min(array)
        self.maximum = max(array)
        self.widthBlock = round((self.width - self.sidePadding) / len(array))
        self.heightBlock = math.floor((self.height - self.topPadding) / (self.maximum - self.minimum))
        self.startPositionX = self.sidePadding // 2
def draw(drawInfo, sortingAlgoName, ascending):
    drawInfo.window.fill(drawInfo.backgroundColor)
    title = drawInfo.fontTwo.render(f"{sortingAlgoName} - {'Ascending' if ascending else 'Descending'}", 1, drawInfo.black)
    drawInfo.window.blit(title, (drawInfo.width / 2 - title.get_width() / 2, 0))
    controls = drawInfo.fontOne.render("CONTROLS: A = Ascending, D = Descending, SPACE to sort, R to reset", 1, drawInfo.black)
    drawInfo.window.blit(controls, (drawInfo.width / 2 - controls.get_width() / 2, 45))
    sorting = drawInfo.fontOne.render("1 = Insertion, 2 = Bubble, 3 = Selection", 1, drawInfo.black)
    drawInfo.window.blit(sorting, (drawInfo.width / 2 - sorting.get_width() / 2, 75))
    drawArray(drawInfo)
    pygame.display.update()
def drawArray(drawInfo, colorPositions = {}, clearBackground = False):
    array = drawInfo.array
    if clearBackground:
        clearRect = (drawInfo.sidePadding // 2, drawInfo.topPadding, drawInfo.width - drawInfo.sidePadding, drawInfo.height - drawInfo.topPadding)
        pygame.draw.rect(drawInfo.window, drawInfo.backgroundColor, clearRect)
    for i, val in enumerate(array):
        x = drawInfo.start_x + i * drawInfo.blockWidth
        y = drawInfo.height - (val - drawInfo.minVal) * drawInfo.blockHeight
        color = drawInfo.gradients[i * 3]
        if i in colorPositions:
            color = colorPositions[i]
        pygame.draw.rect(drawInfo.window, color, (x, y, drawInfo.blockWidth, drawInfo.height))
    if clearBackground:
        pygame.display.update()
def generateStartingList(n, minimum, maximum):
    array = []
    for _ in range(n):
        value = random.randint(minimum, maximum)
        array.append(value)
    return array
def bubbleSort(drawInfo, ascending = True):
    array = drawInfo.array
    for i in range(len(array) - 1):
        for j in range(len(array)- 1 - i):
            num1 = array[j]
            num2 = array[j + 1]
            if(num1 > num2 and ascending) or (num1 < num2 and not ascending):
                array[j], array[j + 1] = array[j + 1], array[j]
                drawArray(drawInfo, {j: drawInfo.GREEN, j + 1: drawInfo.RED}, True)
                yield True
    return array
def insertionSort(drawInfo, ascending = True):
    array = drawInfo.array
    for i in range(1, len(array)):
        currentNum = array[i]
        while True:
            ascendingSort = i > 0 and array[i - 1] > currentNum and ascending
            descendingSort = i > 0 and array[i - 1] > currentNum and not ascending
            if not ascendingSort and not descendingSort:
                break
            array[i] = array[i - 1]
            i = i - 1
            array[i] = currentNum
            drawArray(drawInfo, {i: drawInfo.GREEN, i - 1: drawInfo.RED}, True)
            yield True
    return array
def selectionSort(drawInfo, ascending = True):
    array = drawInfo.array
    size = len(array)
    for i in range(size - 1):
        minIndex = i
        for j in range(minIndex + 1, size):
            if(array[j] > array[minIndex] and not ascending) or (array[j] < array[minIndex] and ascending):
                minIndex = j
            array[i], array[minIndex] = array[minIndex], array[i]
            drawArray(drawInfo, {j - 1: drawArray. GREEN, j: drawArray.RED}, True)
            yield True
    return array
def main():
    run = True
    clock = pygame.time.Clock()
    n = 100 #Element Numbers to sort
    minimumValue = 1 
    maximumValue = 100
    array = generateStartingList(n, minimumValue, maximumValue)
    drawInfo = drawInformation(1024, 500, array)
    sorting = False
    ascending = True
    sortingAlgorithm = bubbleSort
    sortingAlgorithmName = "Bubble Sort"
    sortingAlgorithmGenerator = None
    while run: 
        clock.tick(120)
        if sorting:
            try:
                next(sortingAlgorithmGenerator)
            except StopIteration:
                sorting = False
        else:
            draw(drawInfo, sortingAlgorithmName, ascending)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                array = generateStartingList(n, minimumValue, maximumValue)
                drawInfo.setList(array)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sortingAlgorithmGenerator = sortingAlgorithm(drawInfo, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_1 and not sorting:
                sorting_algorithm = insertionSort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_2 and not sorting:
                sorting_algorithm = bubbleSort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_3 and not sorting:
                sorting_algorithm = selectionSort
                sorting_algo_name = "Selection Sort"
    pygame.quit()            

if __name__ == "__main__":
    main()