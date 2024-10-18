import tkinter as tk
from tkinter.messagebox import showinfo
import random

class Snake:

    def __init__(self):
        #初始化
        # self.debugprint()
        self.window=None
        
        self.canvas=None
        self.loop_id=None
        
        self.map=[]                      #二维列表表示地图
        self.body=[]                     #二维列表表示蛇身坐标集
        self.apple=[]                    #苹果的坐标集，包含xy两项
        

        self.suspend=0                   #暂停键，0是暂停，1是继续

        self.direct=0                    #方向，0是上下1是左右按坐标系
        
        self.goal=100                    #目标分数，默认100
        self.score=0                     #当前分数

        self.FPS=100                     #速度
        self.initlen=3                   #初始和当前长度
        self.len=self.initlen
        
        self.square_row=27
        self.square_col=27               #行列数
        self.square_size=20              #方格大小
        self.square_gap=0                #方格间距
        self.win_extra=120


        self.head=[self.square_col // 2, self.square_row// 2]    #头的坐标，head[0]是x,head[1]是y
        #print(self.head)

        #对颜色，备查
        self.colordict={
           
            1: 'blue',              # 蛇头
            2: 'black',             # 蛇身
            3: 'red',               # 苹果
            4: 'gray',              # 墙
            0: 'white',             # 空地

         }

        self.inquiry_()                    #询问用户目标分数，到达暂停

        

    #以下保证没有问题就不要查了    

    def inquiry_(self):

        def iqy():
            entry=qentry.get()
            if not entry:self.goal=100
            else:self.goal=qentry.get()
            #print(self.goal)
            qwindows.destroy()

            
        qwindows=None
        qwindows=tk.Tk()
        qwindows.focus_force()
        qwindows.title("询问界面")

        wWidth = qwindows.winfo_screenwidth()
        wHeight = qwindows.winfo_screenheight()
        wwwww=(wWidth-500)//2
        hhhhh=(wHeight-300)//2
        qwindows.geometry("{}x{}+{}+{}".format(500,300,wwwww,hhhhh))

        qlabel=tk.Label(qwindows,text="请输入目标分数（输入后点击确定）(默认100）：")
        qlabel.pack(pady=20)

        qentry=tk.Entry(qwindows)
        qentry.pack(pady=10)

        qbutton=tk.Button(qwindows,text="确定",command=iqy)    #之后可以用bind写暂停按钮
        qbutton.pack(pady=20)

        #qwindows.bind('<Enter>', iqy)

        qwindows.mainloop()

        self.game_start()

    #以上保证没有问题无需检查
        


    def game_start(self):
        
        self.window=tk.Tk()
        self.window.focus_force()
        self.window.title("贪吃蛇")

        Width = self.square_row*self.square_size+30+self.win_extra      
        Height = self.square_col*self.square_size+30                   #30是边框上下
        wwwwww=(self.window.winfo_screenwidth()-Width)//2
        whhhhh=(self.window.winfo_screenheight()-Height)//2
        self.window.geometry("{}x{}+{}+{}".format(Width,Height,wwwwww,whhhhh))
 
        self.canvas = tk.Canvas(self.window, bg='white', height=Height, width=Width-self.win_extra, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        txt_lable = tk.Label(self.window, text="操作方式:\n(W)向上\n(S)向下\n(A)向左\n(D)向右\n(Space)暂停", font=('Fang_song', 15))
        txt_lable.place(x=self.square_size * self.square_col + self.square_size * 2, y=self.square_size * 10)

        self.game_next()



    def draw_map(self):

        #创建二维列表
        self.map=[]
        for i in range(0,self.square_col):
            self.map.append([])
        for i in range(0,self.square_col):
            for j in range(0,self.square_row):
                self.map[i].append(j)
                self.map[i][j]=0

        #画墙

        for i in range(0, self.square_col - 1): 
            self.map[0][i] = 4
            self.map[self.square_col - 1][i] = 4
 
        for i in range(0, self.square_row - 1):
            self.map[i][0] = 4
            self.map[i][self.square_row - 1] = 4
            
        self.map[-1][-1] = 4


    

    def draw(self):

        for i in range(0, self.square_col):
            for j in range(0, self.square_row):
                
                a = 15 + self.square_size * j
                b = 15 + self.square_size * i
                c = 15 + self.square_size * (j + 1)
                d = 15 + self.square_size * (i + 1)
                e = 'white'
                f = self.square_gap
                g = self.colordict[self.map[i][j]]
                self.canvas.itemconfig(self.canvas.create_rectangle(a, b, c, d, outline=e, width=f, fill=g), fill=g)


    def draw_snake(self):
        self.head=[self.square_col // 2, self.square_row// 2]
        # 蛇头
        self.body = [[self.square_col // 2, self.square_row// 2]]
        # 蛇身 蛇头 上色
        self.map[self.body[0][0]][self.body[0][1]] = 1
        #print(self.body)

    def draw_apple(self):

        self.apple=[0,0]
        self.apple[0] = random.randint(1, self.square_col - 2)
        self.apple[1] = random.randint(1, self.square_row - 2)
        
        while self.map[self.apple[0]][self.apple[1]] !=0:
            self.apple[0] = random.randint(1, self.square_col - 2)#留一个加速苹果的念想
            self.apple[1] = random.randint(1, self.square_row - 2)

        print (self.apple)
        self.map[self.apple[0]][self.apple[1]] = 3


    def find_head(self):

        xy = []
        #print(self.head)
        #print(3)
        for i in range(0, self.square_col):
            try:  
                x = self.map[i].index(1) + 1
            except:
                x = 0
            xy.append(x)
        #print (xy)
        self.head[0] = max(xy) #找x
        self.head[1] = xy.index(self.head[0])
        self.head[0] = self.head[0] - 1



    def move_snake(self,event):


        def move(a,b,c,d):
            direction= event.keysym
            #检测头和身子是否相同，若相同则不执行转向命令，防止头钻进肚子里
            ###
            if self.head[0] != self.body[-1][0]:
                if direction == a:
                    self.direct = 1
                if direction == b:
                    self.direct = 2
            else:
                if direction == c:
                    self.direct = 3
                if direction == d:
                    self.direct = 4
 
            if self.head[1] != self.body[-1][1]:
                if direction == c:
                    self.direct = 3
                if direction == d:
                    self.direct = 4
            else:
                if direction == a:
                    self.direct = 1
                if direction == b:
                    self.direct = 2
            ###
        def pause(n):
            direction= event.keysym
            if direction==n:
                self.suspend = 0
                showinfo('暂停', '按确定键继续')
                self.suspend = 1
                self.window.after(self.FPS, self.suspend_loop)


        move('w','s','a','d')
        move('W', 'S', 'A', 'D')
        move('Up', 'Down', 'Left', 'Right')
        pause('space')
        

    def game_over(self):
 
        def over():
            showinfo('游戏结束', '本次得分: {}\n\n是否再来一局?'.format(self.score))
            # 判断分数
            self.score = 0
            self.body_len = self.len
            self.window.destroy()
            self.inquiry_()
            #print(self.goal)

        ###
        if [self.head[0], self.head[1]] in self.body[0:-2]: over()
        if self.head[0] == self.square_row - 1 or self.head[0] == 0:
            #print(self.head)
            over()
        if self.head[1] == self.square_col - 1 or self.head[1]== 0:
            #print(self.head)
            over()


     
        if self.score==self.goal:
            #print(self.goal)
            showinfo('游戏结束', '本次得分: {}\n\n达到目标，是否再来一局?'.format(self.score))
            # 判断分数
            self.score = 0
            self.body_len = self.len
            self.inquiry_()


    def snake_record(self):
        
        temp=[]
        temp.append(self.head[0])
        temp.append(self.head[1])
        self.body.append(temp)
        if self.body[-1]==self.body[-2]:
            del self.body[-1]
        
        if [self.head[1],self.head[0]]==self.apple:
            print (1)
            self.score += 1
            self.len += 1
            self.draw_apple()
        elif len(self.body) > self.len:
            self.map[self.body[0][1]][self.body[0][0]] = 0
            del self.body[0]
            
        def move(d, x, y):
            if self.direct == d:  # 根据方向值来决定走向
                self.map[self.head[1] + x][self.head[0] + y] = 1
                self.map[self.head[1] + 0][self.head[0] + 0] = 2
 
        move(1, -1, 0)
        move(2, 1, 0)
        move(3, 0, -1)
        move(4, 0, 1)
    
    def suspend_loop(self):

        self.snake_record()
        self.find_head()
        #改名防撞
        self.canvas.delete('all')
        self.draw()
        self.game_over()

        ###
        if self.suspend == 1:
            txt_s = tk.Label(self.window, text="\n\n当前得分:\n({})\n\n".format(self.score), font=('Ya_hei', 15))
            txt_s.place(x=self.square_size * self.square_col + self.square_size * 2, y=self.square_size * 2)
            self.loop_id = self.window.after(self.FPS, self.suspend_loop)
        ###

    def game_next(self):

        self.suspend=1
        self.direct=0

        self.draw_map()
        self.draw_snake()
        self.draw_apple()

        #print(self.head)
        #print('2')

        self.find_head()
        self.window.bind('<Key>', self.move_snake)
        self.suspend_loop()
        
        def winclose():
            self.suspend = 0
            self.window.after_cancel(self.loop_id)
            self.window.destroy()
 
        self.window.protocol('WM_DELETE_WINDOW', winclose)
        #self.qwindows.mainloop()
        self.window.mainloop()
        

    '''
    def debugprint(self):
        def pr_():
           ar=0
           print("all right")
        pr_()
     '''        

if __name__ == '__main__':
    
    Snake()
