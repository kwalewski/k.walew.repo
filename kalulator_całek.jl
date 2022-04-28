#Wykonawcy:
#-Krystian Walewski 255773
#-Tymoteusz Kempa 255727
#-Michał Butmankiewicz 255751

using Gtk
using Plots
using QuadGK

#--------------------------------------------------
#Inicjalizacja gui
#--------------------------------------------------

win = GtkWindow("Kalkulator Całek",700, 600)
g = GtkGrid()

#definiujemy wszystkie guziki i pola
formula = GtkEntry()
start = GtkButton("oblicz")
choice_List = GtkComboBoxText()
left_Range = GtkEntry()
right_Range = GtkEntry()
precision = GtkEntry()
label = GtkLabel("Wynik Całki:")
empty = GtkLabel(" ")
zamknij = GtkButton("EXIT")

set_gtk_property!(precision, :text, "Dokładnośc (ilość kropek/słupków)")
set_gtk_property!(formula, :text, "Wpisz wzór funkcji(np. x^2)")
set_gtk_property!(left_Range, :text, "Przedział od")
set_gtk_property!(right_Range, :text, "Przedział do")

#ustawiamy listę rozwijaną
choices = ["Wybierz metodę liczenia","Metoda MonteCarlo",
           "Metoda Riemann'a-wartość min","Metoda Riemann'a-wartość max",
           "Metoda Riemann'a-średnia artmetyczna",
           "Metoda Riemann'a-początek przedziału",
           "Metoda Riemann'a-koniec przedziału",
           "Metoda Riemann'a-porównanie metod"]

for choice in choices
    push!(choice_List,choice)
end

set_gtk_property!(choice_List,:active,0)

#zmienna c będzie mówiła, która metoda została wybrana
signal_connect(choice_List, "changed") do widget, others...
    global c = get_gtk_property(choice_List, "active", Int)
end
signal_connect(zamknij, :clicked) do widget
    Gtk.destroy(win)
end
#ustawiamy wszystko na swoje miejsce
g[1:2,1] = formula
g[1:2,4] = start
g[2,3] = choice_List
g[1,2] = left_Range
g[2,2] = right_Range
g[1,3] = precision
g[1:2,5] = empty
g[1,6] = label
g[3,1:4]=zamknij


#------------------------------------------------------
#Funkcje dla metod
#------------------------------------------------------
function montecarlo(n,a,b,f::Function)

    #--------------------------------------------------
    #Będziemy za każdym razem czyścić okno i dodawać do niego
    #wszystkie rzeczy, aby wyświetlić nowy wykres
    destroy(g)

    global formula = GtkEntry()
    start = GtkButton("oblicz")
    choice_List = GtkComboBoxText()
    global left_Range = GtkEntry()
    global right_Range = GtkEntry()
    global precision = GtkEntry()
    label = GtkLabel("Wynik Całki:")
    empty = GtkLabel(" ")
    zamknij=GtkButton("EXIT")

    set_gtk_property!(precision, :text, "$n")
    set_gtk_property!(formula, :text, "$formula1")
    set_gtk_property!(left_Range, :text, "$a1")
    set_gtk_property!(right_Range, :text, "$b1")

    choices = ["Wybierz metodę liczenia","Metoda MonteCarlo",
               "Metoda Riemann'a-wartość min","Metoda Riemann'a-wartość max",
               "Metoda Riemann'a-średnia artmetyczna",
               "Metoda Riemann'a-początek przedziału",
               "Metoda Riemann'a-koniec przedziału",
               "Metoda Riemann'a-porównanie metod"]

    for choice in choices
        push!(choice_List,choice)
    end

    set_gtk_property!(choice_List,:active,c)
    signal_connect(choice_List, "changed") do widget, others...
        global c = get_gtk_property(choice_List, "active", Int)
    end
    signal_connect(zamknij, :clicked) do widget
        Gtk.destroy(win)
    end

    g[1:2,1] = formula
    g[1:2,4] = start
    g[2,3] = choice_List
    g[1,2] = left_Range
    g[2,2] = right_Range
    g[1,3] = precision
    g[1:2,5] = empty
    g[1,6] = label
    g[3,1:4]=zamknij

    set_gtk_property!(g, :column_homogeneous, true)
    set_gtk_property!(g, :column_spacing, 15)

    id = signal_connect(rysuj, start, "clicked")
    #-------------------------------------------------

    xs = LinRange(a, b, 1000)
    ys = f.(xs)
    zera = zeros(1000)

    #rysyjemy wykres funkcji
    wykres_MC = plot(xs, ys,
        c = :orange,
        title = "Obliczanie całki metodą Monte Carlo dla $n punktow",
        legend = false,
        linewidth = 3,
        linecolor = :black,
        fillrange = [zera ys],
        fillalpha = 0.2)

    #wsp. x losowych punktów na obszarze
    Points_X = (rand(n) .* (b-a)) .+ a

    #Przedział wsp. y punktów jest różny dla 3 przypadków
    if minimum(ys) > 0
        Points_Y = rand(n) .* maximum(ys)
    elseif maximum(ys) < 0
        Points_Y = rand(n) .* minimum(ys)
    else
        Points_Y = (rand(n) .* (maximum(ys)-minimum(ys))) .+ minimum(ys)
    end

    #wartosci funkcji dla naszych losowych x
    Points_X_Values = f.(Points_X)

    #sprawdzamy które wartości są wieksze o zera i definiujemy nowe listy dla nich
    #tworząc kolejne maski. Będziemy wybierać tylko te punkty, które w danym
    #przypadku nas interesują. Na początku srawdzamy, które punkty leżą nad
    #osią x. Potem sprawdzamy czy leży nad wykresem czy pod nim.
    #Analogicznie robimy dla punktów pod osią x
    Mask1 = Points_Y .> 0
    Points_Y_Plus = Points_Y[Mask1]
    Points_X_Plus = Points_X[Mask1]
    Points_X_Values_Plus = Points_X_Values[Mask1]

    #Sprawdzamy które wartości dla tych wybranych punktów są pod, a ktąre nad wykresem
    Mask2 = Points_Y_Plus .>= Points_X_Values_Plus
    Points_Y_Plus_Bad = Points_Y_Plus[Mask2]
    Points_X_Plus_Bad = Points_X_Plus[Mask2]

    Mask3 = Points_Y_Plus .< Points_X_Values_Plus
    Points_Y_Plus_Good = Points_Y_Plus[Mask3]
    Points_X_Plus_Good = Points_X_Plus[Mask3]

    #to samo dla mniejszych od 0
    Mask4 = Points_Y .<= 0
    Points_Y_Minus = Points_Y[Mask4]
    Points_X_Minus = Points_X[Mask4]
    Points_X_Values_Minus = Points_X_Values[Mask4]

    Mask5 = Points_Y_Minus .<= Points_X_Values_Minus
    Points_Y_Minus_Bad = Points_Y_Minus[Mask5]
    Points_X_Minus_Bad = Points_X_Minus[Mask5]

    Mask6 = Points_Y_Minus .> Points_X_Values_Minus
    Points_Y_Minus_Good = Points_Y_Minus[Mask6]
    Points_X_Minus_Good = Points_X_Minus[Mask6]

    Points_X_Bad = [Points_X_Minus_Bad ; Points_X_Plus_Bad]
    Points_Y_Bad = [Points_Y_Minus_Bad ; Points_Y_Plus_Bad]

    #Nanosimy każdą grupę punktów na wykres
    scatter!(Points_X_Plus_Good, Points_Y_Plus_Good,
            markersize=1, markerstrokewidth=0, c=:blue)
    scatter!(Points_X_Bad, Points_Y_Bad,
            markersize=1, markerstrokewidth=0, c=:red)
    scatter!(Points_X_Minus_Good,Points_Y_Minus_Good,
            markersize=1, markerstrokewidth=0, c=:green)

    #Liczymy pole obszaru
    if minimum(ys) > 0
        P_Rect = (b-a)*maximum(ys)
    elseif maximum(ys) < 0
        P_Rect = (b-a)*(-minimum(ys))
    else
        P_Rect = (b-a)*(maximum(ys)-minimum(ys))
    end

    #liczymy wartość całki i wyswietlamy ją
    percent = length(Points_X_Plus_Good) - length(Points_X_Minus_Good)
    Integral_MC = percent/n * P_Rect
    GAccessor.text(label,"Wynik Całki: $Integral_MC")

    #zapisujemy wykres i wyświetlamy go w interfejsie
    savefig("wykres.png")
    a = GtkImage("wykres.png")
    g[1:2,7] = a
    push!(win,g)
    showall(win)
end


function rieman(n,a,b,f::Function,c)

    #--------------------------------------------------
    destroy(g)

    global formula = GtkEntry()
    start = GtkButton("oblicz")
    choice_List = GtkComboBoxText()
    global left_Range = GtkEntry()
    global right_Range = GtkEntry()
    global precision = GtkEntry()
    label = GtkLabel("Wynik Całki:")
    empty = GtkLabel(" ")
    zamknij=GtkButton("EXIT")

    set_gtk_property!(precision, :text, "$n")
    set_gtk_property!(formula, :text, "$formula1")
    set_gtk_property!(left_Range, :text, "$a1")
    set_gtk_property!(right_Range, :text, "$b1")

    choices = ["Wybierz metodę liczenia","Metoda MonteCarlo",
               "Metoda Riemann'a-wartość min","Metoda Riemann'a-wartość max",
               "Metoda Riemann'a-średnia artmetyczna",
               "Metoda Riemann'a-początek przedziału",
               "Metoda Riemann'a-koniec przedziału",
               "Metoda Riemann'a-porównanie metod"]

    for choice in choices
        push!(choice_List,choice)
    end

    set_gtk_property!(choice_List,:active,c)
    signal_connect(choice_List, "changed") do widget, others...
        global c = get_gtk_property(choice_List, "active", Int)
    end
    signal_connect(zamknij, :clicked) do widget
        Gtk.destroy(win)
    end

    g[1:2,1] = formula
    g[1:2,4] = start
    g[2,3] = choice_List
    g[1,2] = left_Range
    g[2,2] = right_Range
    g[1,3] = precision
    g[1:2,5] = empty
    g[1,6] = label
    g[3,1:4] = zamknij

    set_gtk_property!(g, :column_homogeneous, true)
    set_gtk_property!(g, :column_spacing, 15)

    id = signal_connect(rysuj, start, "clicked")
    #-------------------------------------------------

    #wartości potrzebne do narysowania wykresu funcji
    xs = LinRange(a,b,1000)
    ys = f.(xs)

    #wartości potrzebne do narysowania prostokątów
    xd = LinRange(a,b,n+1) #punkty podziału
    yd = f.(xd) #wartości dla tych punktów

    wykres_R = plot(xs, ys,
        c = :orange,
        title = "Obliczanie całki metodą Riemann'a dla $n prostokątow",
        legend = false,
        linewidth = 3,
        linecolor = :black)

    #Teraz wybieramy w którym punkcie nasz prostokąt styka się z
    #wykresem funkcji(inaczej-wysokość słupka).Jednocześnie rysujemy
    #te słupki i liczymy wynik.

    #definiujemy długość przedziału, którą będziemy mnożyć przez wys. słupka
    range_Length = xd[2] - xd[1]
    range_Lengths = fill(range_Length, n)

    if c == 4 #Średnia arytmetyczna początku przedziału i końca
        #definiujemy wszystkie wysokości słupków
        heights = (yd[2:end] .+ yd[1:end-1]) ./ 2

        #sumujemy wszystkie pola
        outcome = sum(range_Lengths .* heights)

        #definiujemy zakresy potrzebne do stworzenia wykresów prostokątów
        #Dlatego też wartości muszą się w nich powtarzać np. 1,2,2,3,3,4
        #dla osi x i np. 1,1,5,5,3,3 dla osi y
        e = zeros(2n+2)
        e[1:2:2n+1] = xd[1:end]
        e[2:2:2n+2] = xd[1:end]

        p = zeros(2n)
        p[1:2:2n-1] = heights[1:end]
        p[2:2:2n] = heights[1:end]

        plot!(e[2:end-1], p, fillrange=[[0,0],[100,100]],
              color=:reds, fillalpha=0.9)

    elseif c == 5 #początek przedziału
        heights = yd[1:end-1]

        outcome = sum(range_Lengths .* heights)

        e = zeros(2n+2)
        e[1:2:2n+1] = xd[1:end]
        e[2:2:2n+2] = xd[1:end]

        p = zeros(2n)
        p[1:2:2n-1] = heights[1:end]
        p[2:2:2n] = heights[1:end]

        plot!(e[2:end-1], p, fillrange=[[0,0],[100,100]],
              color=:reds, fillalpha=0.9)

    elseif c == 6 #koniec przedziału
        heights = yd[2:end]

        outcome = sum(range_Lengths .* heights)

        e = zeros(2n+2)
        e[1:2:2n+1] = xd[1:end]
        e[2:2:2n+2] = xd[1:end]

        p = zeros(2n)
        p[1:2:2n-1] = heights[1:end]
        p[2:2:2n] = heights[1:end]

        plot!(e[2:end-1], p, fillrange=[[0,0],[100,100]],
              color=:reds, fillalpha=0.9)

    elseif c == 3 #wartość maksymalna na przedziale
        heights = max.(yd[1:end-1],yd[2:end])

        outcome = sum(range_Lengths .* heights)

        e = zeros(2n+2)
        e[1:2:2n+1] = xd[1:end]
        e[2:2:2n+2] = xd[1:end]

        p = zeros(2n)
        p[1:2:2n-1] = heights[1:end]
        p[2:2:2n] = heights[1:end]

        plot!(e[2:end-1], p, fillrange=[[0,0],[100,100]],
              color=:reds, fillalpha=0.9)

    elseif c == 2 #minimalna
        heights = min.(yd[1:end-1],yd[2:end])

        outcome = sum(range_Lengths .* heights)

        e = zeros(2n+2)
        e[1:2:2n+1] = xd[1:end]
        e[2:2:2n+2] = xd[1:end]

        p = zeros(2n)
        p[1:2:2n-1] = heights[1:end]
        p[2:2:2n] = heights[1:end]

        plot!(e[2:end-1], p, fillrange=[[0,0],[100,100]],
              color=:reds, fillalpha=0.9)
    end

    GAccessor.text(label,"Wynik Całki: $outcome")

    savefig("wykres.png")
    a = GtkImage("wykres.png")
    g[1:2,7] = a
    push!(win,g)
    showall(win)
end


function compare(n,a,b,f::Function)

    #--------------------------------------------------
    destroy(g)

    global formula = GtkEntry()
    start = GtkButton("oblicz")
    choice_List = GtkComboBoxText()
    global left_Range = GtkEntry()
    global right_Range = GtkEntry()
    global precision = GtkEntry()
    label = GtkLabel("Wynik Całki:")
    empty = GtkLabel(" ")
    zamknij=GtkButton("EXIT")

    set_gtk_property!(precision, :text, "$n")
    set_gtk_property!(formula, :text, "$formula1")
    set_gtk_property!(left_Range, :text, "$a1")
    set_gtk_property!(right_Range, :text, "$b1")

    choices = ["Wybierz metodę liczenia","Metoda MonteCarlo",
               "Metoda Riemann'a-wartość min","Metoda Riemann'a-wartość max",
               "Metoda Riemann'a-średnia artmetyczna",
               "Metoda Riemann'a-początek przedziału",
               "Metoda Riemann'a-koniec przedziału",
               "Metoda Riemann'a-porównanie metod"]

    for choice in choices
        push!(choice_List,choice)
    end

    set_gtk_property!(choice_List,:active,c)
    signal_connect(choice_List, "changed") do widget, others...
        global c = get_gtk_property(choice_List, "active", Int)
    end
    signal_connect(zamknij, :clicked) do widget
        Gtk.destroy(win)
    end

    g[1:2,1] = formula
    g[1:2,4] = start
    g[2,3] = choice_List
    g[1,2] = left_Range
    g[2,2] = right_Range
    g[1,3] = precision
    g[1:2,5] = empty
    g[1,6] = label
    g[3,1:4] = zamknij

    set_gtk_property!(g, :column_homogeneous, true)
    set_gtk_property!(g, :column_spacing, 15)

    id = signal_connect(rysuj, start, "clicked")
    #-------------------------------------------------


    #liczymy dokładną wartość całki
    range = [1,2,3,4,5,6]
    exact_outcome = quadgk(f,a,b,rtol=1e-3)
    exact_otcomes = fill(exact_outcome[1],6)

    xd = LinRange(a,b,n+1)
    yd = f.(xd)

    range_Length = xd[2] - xd[1]
    range_Lengths = fill(range_Length, n)

    #liczymy wartość całek dla każdej z metod
    outcome1 = sum(range_Lengths .* ((yd[2:end] .+ yd[1:end-1]) ./ 2))
    outcome2 = sum(range_Lengths .* yd[1:end-1])
    outcome3 = sum(range_Lengths .* yd[2:end])
    outcome4 = sum(range_Lengths .* max.(yd[1:end-1],yd[2:end]))
    outcome5 = sum(range_Lengths .* min.(yd[1:end-1],yd[2:end]))

    #Nasz dokładny wynik nanosimy jako linie poziomą.
    Wykres2 = plot(range,exact_otcomes,
        title="Dokładność całki Riemann'a dla $n punktow",
        color=:black,
        linewidth=2,
        xticks=([],[]),
        label="dokładny wynik",
        legend=:outerright)

    #nanosimy słupki na wykres
    plot!([1,2],[outcome1,outcome1],fillrange=[[0,0],[10,10]],
                fillalpha=0.6,label="średnia artmetyczna")
    plot!([2,3],[outcome2,outcome2],fillrange=[[0,0],[10,10]],
                fillalpha=0.6,label="początek przedziału")
    plot!([3,4],[outcome3,outcome3],fillrange=[[0,0],[10,10]],
                fillalpha=0.6,label="koniec przedziału")
    plot!([4,5],[outcome4,outcome4],fillrange=[[0,0],[10,10]],
                fillalpha=0.6,label="wartość max")
    plot!([5,6],[outcome5,outcome5],fillrange=[[0,0],[10,10]],
                fillalpha=0.6,label="wartość min")


    GAccessor.text(label,"Wynik Całki: $(exact_outcome[1])")

    savefig("wykres.png")
    a = GtkImage("wykres.png")
    g[1:4,7] = a
    push!(win,g)
    showall(win)
end


#------------------------------------------------------
#uruchomienie rysowania i liczenia
#------------------------------------------------------

function rysuj(widget)

    #Pobieramy wartości zmiennych
    global formula1 = get_gtk_property(formula,:text,String)
    global a1 = get_gtk_property(left_Range,:text,String)
    global b1 = get_gtk_property(right_Range,:text,String)
    n1 = get_gtk_property(precision,:text,String)

    #zmieniamy string na float
    a2 = parse(Float64, a1)
    b2 = parse(Float64, b1)
    n2 = parse(Int64, n1)

    #Jako, że wzór funkcji podaliśmy jako string
    #musimy go przekształcić w pełnoprawną funkcje
    function fcnFromStr(s)
        f = eval(Meta.parse("x -> " * s))
        return x -> Base.invokelatest(f,x)
    end

    function g(x)
        f = fcnFromStr(formula1)
        return f(x)
    end

    #w zależności od wybranej metody, uruchamiamy funkcje
    if c == 1
        montecarlo(n2, a2, b2, g)
    elseif c == 7
        compare(n2, a2, b2, g)
    else
        rieman(n2, a2, b2, g, c)
    end
end

set_gtk_property!(g, :column_homogeneous, true)
set_gtk_property!(g, :column_spacing, 15)

id = signal_connect(rysuj, start, "clicked")

push!(win, g)
showall(win)
