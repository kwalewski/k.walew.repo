#--------------------------------------------------------------------
#KRYSTIAN WALEWSKI 255773
#--------------------------------------------------------------------
using Plots

pierwiastki(z, n) = begin

    #Sprawdzamy czy liczba n jest całkowita i większa od 1.
    if n >= 2 && isinteger(n)
        println("Pierwiastki $n stopnia liczby zespolonej $z:")
    else
        error("Liczba pierwiastków musi być całkowita i większa od 1")

    end

    #-----------------------------------------------------------------
    #Promień i argument liczby z potrzebny do wyznaczenia pierwiastków.
    r = abs(z)
    argz = angle(z)

    #Potzebny będzie też pierwiastek n-go stopnia z r.
    root_r = r^(1/n)
    #----------------------------------------------------------------


    #----------------------------------------------------------------
    #Pierwszy pierwiastek.
    w1 = root_r*(cos(argz/n) + sin(argz/n)im)

    #Wyznaczamy teraz resztę pierwiastków.
    #Tworzymy listę z wartością przez którą będziemy mnożyć
    #każdy kolejny pierwiastek. Na pierwsze miejsce wstawiamy
    #pierwszy pierwiastek.
    a = fill(cos(2pi/n) + sin(2pi/n)*im, n)
    a[1] = w1

    #Z pomocą komendy accumulate otrzymujemy wszystkie pierwiastki.
    pierwiastki = accumulate(*, a)

    #Wyprintujemy też wszystkie pierwiastki do konsoli.
    index = 1:n
    w = fill("w", n)
    equal = fill("=", n)
    println.(w, index, equal, round.(pierwiastki, digits = 2))
    #-----------------------------------------------------------------


    #-----------------------------------------------------------------
    #Dodajemy naszą liczbę z na początek listy z pierwiastkami.
    prepend!(pierwiastki, z)

    #Na potrzeby wykresu bedziemy tworzyć listy z częściami rzeczywistymi
    #i urojonymi, aby zaimplementować je odpowiednio jako argumenty i
    #odpowiadajace im wartości.
    REAL = real.(pierwiastki)
    IMAG = imag.(pierwiastki)
    #------------------------------------------------------------------


    #------------------------------------------------------------------
    #Wykres zaczniemy od "ułożenia" podpisów wartości (yticks) na osi y,
    #bo chcemy, aby wyświetlały się wraz z literą "i".
    #Zdefiniujemy krok, czyli co jaką wartość będzie podpisywana oś y
    #np.: 1i,2i,3i,.. lub 1i,3i,5i,.. lub 1i,7i,13i,.. itd.
    #Jest to przydatne, gdy będziemy rozpatrywać liczby o "dużej"
    #części urojonej. Mając listę wszystkich części urojonych znajdujemy
    #najwiekszą i najmniejszą z nich, co pozwoli nam określić jak daleko
    #"wyjechać" z wartościami dla podpisów. Jest to też uzależnione od znaku
    #imag(z). Np dla dodatniej wartości jeden z pierwiastków może mieć
    #część urojoną większą niż liczba z-wtedy szukamy max, ale od dołu
    #wartości będą ograniczone przez pierwiastek n-go stopnia z r.

    #Będziemy wydłużać krok co wielokrotność 10.
    step = floor(abs(imag(z))/10)+1

    #Definiujemy zakresy podpisów.
    if imag(z) > 0
        y_range = -floor(root_r):step:floor(reduce(max,IMAG))
    elseif imag(z) == 0
        y_range = -floor(root_r)-1:step:floor(root_r)+1
    else
        y_range = floor(reduce(min, IMAG)):step:floor(root_r)
    end
    #-------------------------------------------------------------------


    #-------------------------------------------------------------------
    #Na początku rysujemy wykres z naniesioną liczbą z i okręgiem
    #na którym leżą jej pierwiastki.
    f(x) = root_r*sin(x)
    g(x) = root_r*cos(x)
    plot(f,g,-pi,pi,
        label = false,
        style = :dash)

    #Aby wyeliminować w legendzie opis liczby z w stylu 1+-3i modyfikujemy
    # wartość, którą wyświetlimy, w zależności od znaku części urojonej.
    if imag(z) >= 0
        name1 = "z= $(real(z))+$(imag(z))i"
    else
        name1 = "z= $(real(z))$(imag(z))i"
    end

    #Ustalamy z której strony będzie legenda.
    if real(z) >= 0
        LEGEND = :topright
    else
        LEGEND = :topleft
    end

    #Teraz nanosimy liczbę z i ustawiamy wszystkie nazwy osi,
    #poprawną skalę, położenie osi, legendę itp.
    scatter!([REAL[1]], [IMAG[1]],
        ratio = :equal,
        framestyle = :origin,
        legend = LEGEND,
        color = :black,
        label = name1,
        title = "Pierwiastki $n stopnia liczby zespolonej $z",
        xlabel = "Re z",
        ylabel = "Im z",
        yticks = (y_range, string.(y_range) .* "i"))
    #-------------------------------------------------------------------


    #-------------------------------------------------------------------
    #Rozpoczynamy animacje.
    anim = @animate for i=2:n+1

        #Robimy teraz podobną rzecz z etykietami, co poprzednio, ale dla pierwiastków.
        #Jednocześnie zaokrąglamy wyniki i ustalamy dla jakich pierwiastków
        #będą wyświetlane etykiety. Powiedzmy, że maksymalnie może ich być 9.
        #Staramy się jak najbardziej równomiernie rozkładać te podpisy.
        if n > 9
            if (i == floor(n/8) || i == floor(2n/8) || i == floor(3n/8) ||
                i == floor(4n/8) || i == floor(5n/8) ||  i == floor(6n/8) ||
                i == floor(7n/8) ||  i == n || i == 2)
                    if IMAG[i] >= 0
                        name2 = "w$(i-1)= $(round(REAL[i],digits=2))+$(round(IMAG[i],digits=2))i"
                    else
                        name2 = "w$(i-1)= $(round(REAL[i],digits=2))$(round(IMAG[i],digits=2))i"
                    end
            else
                name2 = false
            end
        else
            if IMAG[i] >= 0
                name2 = "w$(i-1)= $(round(REAL[i],digits=2))+$(round(IMAG[i],digits=2))i"
            else
                name2 = "w$(i-1)= $(round(REAL[i],digits=2))$(round(IMAG[i],digits=2))i"
            end
        end

        #Nanosimy kolejne pierwiastki i wybieramy dla nich losowy kolor.
        scatter!([REAL[i]], [IMAG[i]],
                 label = name2,
                 color = RGB(rand(0:255)/255, rand(0:255)/255, rand(0:255)/255))


    end
    #---------------------------------------------------------------------------


    #---------------------------------------------------------------------------
    #liczbę fps będziemy zmieniać podobnie jak kroki.
    #Dla dużego n, będziemy zwiększać liczbę klatek.
    FPS = floor(n/10)+1

    gif(anim, "pierwiastki_z.gif", fps=FPS)
    #---------------------------------------------------------------------------

end

#Przykład wywołania funkcji: pierwiastki(3+5im, 8)
