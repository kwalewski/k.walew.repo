#--------------------------------------------------------------------
#KRYSTIAN WALEWSKI 255773
#--------------------------------------------------------------------
using Plots

#Jako argumenty podajemy funkcję, punkt styczności oraz
#opcjonalnie 3 elementową krotke circle=(x,y,r), albo
#4 elementową rectangle=(a,b,c,d), co oznacza[a,b]x[c,d].
#W ten sposób wyznaczamy naszą dziedzinę, Krotki mają domyślnie
#same zera, aby było wiadomo, którą opcje wybrano.
#Dodatkowo można wybrać wartość h do przybliżania pochodnych
function plaszczyzna(f::Function, point;
                    circle=(0,0,0), rectangle=(0,0,0,0), h = 0.01)

    #współrzędne punktu P0
    x0 = point[1]
    y0 = point[2]
    z0 = f(point[1], point[2])

    #liczymy pochodne cząstkowe w (x0,y0)
    dx = (f(x0+h, y0) - f(x0, y0))/h
    dy = (f(x0, y0+h) - f(x0, y0))/h

    #Równanie płaszczyzny stycznej zapisujemy jako nastepną
    #funkcję 2 zmiennych
    g(x,y) = dx*x - dx*x0 + dy*y - dy*y0 + z0

#---------------------------------------------------------------------

    #Jeśli wybraliśmy prostokąt, to krotka nie będzie równa (0,0,0,0)
    if rectangle != (0,0,0,0)

        a = rectangle[1]
        b = rectangle[2]
        c = rectangle[3]
        d = rectangle[4]

        #sprawdzamy przynależność do dziedziny
        if x0 >= a && x0 <= b && y0 >= c && y0 <= d

            #określamy dziedzinę
            xs = LinRange(a, b, 1000)
            ys = LinRange(c, d, 1000)

            #Aby wykres był przejrzysty i dobrze interpretowany
            #w każdej sytuacji, pokażemy go z różnych kątów.
            #Do tego najlepiej od razu skorzystać z animacji
            anim = @animate for i = 1:50

                #Najpierw nanosimy płaszczyzne styczną i ustawiamy
                #dla niej kolor niebieski, aby się odznaczała
                plot(xs,ys,g,
                    st=:surface,
                    camera=(20+i,10+i),
                    color = cgrad(:blues))

                #Dorysowujemy oryginalną płaszczyznę
                plot!(xs,ys,f,
                    st=:surface,
                    color = cgrad([:red,:yellow,:green]))

                #Stawiamy kropkę
                scatter!([x0], [y0], [z0], legend =:false)
            end

            #zapisujemy animacje
            gif(anim, "płaszczyzna1.gif", fps=15)

        else
            error("Podany punkt nie należy do dziedziny funkcji")
        end

    #Dla koła schemat jest identyczny
    elseif circle != (0,0,0) && circle[3] > 0

        global xo = circle[1]
        global yo = circle[2]
        global ro = circle[3]

        if sqrt((x0-xo)^2 + (y0-yo)^2) <= ro

            #definiujemy funkcje, które pobierają punkt
            #i zwracają jego wartość dla innej funkcji,
            #jeśli należy on do koła
            function circle1(x,y)
                if sqrt((xo-x)^2 + (yo-y)^2) <= ro
                    return f(x,y)
                else
                    return NaN
                end
            end

            function circle2(x,y)
                if sqrt((xo-x)^2 + (yo-y)^2) <= ro
                    return g(x,y)
                else
                    return NaN
                end
            end

            #zakres definiujemy jako kwadrat o boku 2r.
            #Funkcje circle i tak wybierą sobie z tego
            #tylko koło
            xs = LinRange(xo-ro, xo+ro, 1000)
            ys = LinRange(yo-ro, yo+ro, 1000)

            anim = @animate for i = 1:50

                plot(xs,ys,circle2,
                    st=:surface,
                    camera=(20+i,10+i),
                    color = cgrad(:blues))

                plot!(xs,ys,circle1,
                     st=:surface,
                     color = cgrad([:red,:yellow,:green]))

                scatter!([x0], [y0], [z0], legend =:false)
            end

            gif(anim, "płaszczyzna2.gif", fps=15)

        else
            error("Podany punkt nie należy do dziedziny funkcji")
        end

    else
        error("Podano złe parametry funkcji")
    end

end

#Polecam wywołać funkcje bezpośrednio w terminalu niż ją "odhashtagować".
#Wykres rysuje się wtedy dużo szybciej.

#plaszczyzna((x,y)->x^3+y^2-3*x*y, (2,2), rectangle=(-2,3,-1,7))
#plaszczyzna((x,y)->x^2-x*y-y^2, (-1,1), circle=(0,0,4), h=0.0000001)
