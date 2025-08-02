
#define SDL_MAIN_HANDLED

#include <SDL2/SDL.h>
#include <iostream>

int
main(int argc, char* argv[])
{
    if(SDL_Init(SDL_INIT_VIDEO) != 0)
    {
        std::cerr << "SDL_Init Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_Window* win = SDL_CreateWindow("Hello SDL2",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        640,
        480,
        SDL_WINDOW_SHOWN);

    SDL_Delay(2000);
    SDL_DestroyWindow(win);
    SDL_Quit();
    return 0;
}
