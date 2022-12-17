import pygame
import random
import math
pygame.init()

class drawInformation:
    BLACK = 0, 0, 0        #RGB values to denote usage of various colors         
    WHITE = 255, 255, 255
    RED = 255, 0, 0 
    GREEN  = 0, 255, 0
    BLUE = 0, 0, 255
    CYAN = 0, 255, 255
    DARKBLUE = 0, 0, 139
    LIGHTBLUE = 108, 159, 206
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [LIGHTBLUE, CYAN, DARKBLUE]  #creates variation between the randomized rectangles
        
    FONT = pygame.font.SysFont('arial', 30) #text attributes
    LARGEFONT = pygame.font.SysFont('arial', 40)

    SIDE_PAD = 0 #defines sorting area
    TOP_PAD = 200  

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        pygame.display.set_caption("Sorting Algorithm Visualizer - Created by Deep Patel")
        self.window = pygame.display.set_mode((width, height)) #defines window attributes
        
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, sorting_algo_name, ascending):  #user display (selected options are updated in real time)
    draw_info.window.fill(draw_info.BACKGROUND_COLOR) 

    title = draw_info.LARGEFONT.render(f"{sorting_algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 0))

    controls = draw_info.FONT.render("LEGEND: A = Ascending, D = Descending, SPACE = Start, R = Reset", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render("1 = Insertion, 2 = Bubble, 3 = Selection", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions = {}, clear_background = False):
    lst = draw_info.lst

    if clear_background:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_background:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val): #stores randomly generates values of length dimension, for rectangles
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

#any sorting methods can be defined below with a similar setup
def bubble_sort(draw_info, ascending = True):   
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    return lst            


def insertion_sort(draw_info, ascending = True): 
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] > current and not ascending
            if not ascending_sort and not descending_sort:
                break
            
            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i - 1: draw_info.RED}, True)
            yield True
    return lst   


def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst
    size = len(lst)
    for i in range(size-1):
        min_index = i
        for j in range(min_index + 1, size):
            if(lst[j] > lst[min_index] and not ascending) or (lst[j] < lst[min_index] and ascending):
                min_index = j
            lst[i], lst[min_index] = lst[min_index], lst[i]
        draw_list(draw_info, {j - 1: draw_info. GREEN, j: draw_info.RED}, True)  
        yield True
    return lst
  

def main(): 
    run = True
    clock = pygame.time.Clock()

    n = 100 #set the number of elements to be sorted
    min_val = 1         #dimensions of rectangle height
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = drawInformation(1024, 500, lst)  #window dimensions
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    
    while run:
        clock.tick(120)   #parameter which adjusts speed of sorting visualization

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:     #keyboard inputs to control the program
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_1 and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_2 and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_3 and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
    pygame.quit()            

if __name__ == "__main__":
    main()