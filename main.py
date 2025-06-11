import pygame
from Graphic.Screen.Quit import Quit
from Graphic.Screen.Main import Main
from Graphic.Screen.Change_user import ChangeUser
from Graphic.Screen.Recommend import Reccomend
from Graphic.Screen.Rating import Rating
from App.State_Manager import StateManager
from Graphic.Component import Constaint as cs
from App.APP import App

if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption("Gợi ý phim")
        display = pygame.display.set_mode((cs.DISPLAY_WEIGHT,cs.DISPLAY_HEIGHT))
        w,h = display.get_size()

        main = Main(display,(w,h))
        recommend = Reccomend(display,(w,h))
        rating = Rating(display,(w,h))
        change_user = ChangeUser(display,(w,h))
        Quit = Quit

        flag_manager = StateManager(("main","quit","recommend","rate","Change_user"),(main, Quit,recommend,rating,change_user),"Change_user","quit")

        genres = {
                'Action': 0
                , 'Adventure': 1
                , 'Animation': 2
                , "Children": 3
                , 'Comedy': 4
                , 'Crime': 5
                , 'Documentary': 6
                , 'Drama': 7
                , 'Fantasy': 8
                , 'Film-Noir': 9
                , 'Horror': 10
                , 'Musical': 11
                , 'Mystery': 12
                , 'Romance': 13
                , 'Sci-Fi': 14
                , 'Thriller': 15
                , 'War': 16
                , 'Western': 17
                , 'IMAX': 18
            }

        path = {
                'rating': r'Data\rating.h5',
                'movies': r'Data\movies.csv',
                'users': r'Data\users.csv',
                'users_isSeen': r'Data\users_isSeen.h5',
                'users_weight':r'Data\users_weight.h5'
            }

        app = App(flag_manager,path,genres)
        app.run()