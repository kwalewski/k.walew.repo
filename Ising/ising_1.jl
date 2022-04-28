ising_1(T,L) = begin

    J=1
    K_B=1

    S = rand([-1,1],L,L)


    b = [x for x in 1:L]
    prepend!(b,L)
    append!(b,1)

    delta_E = [-8,-4,0,4,8]
    Exp = zeros(17)
    for k in delta_E
        Exp[k+9] = exp(-k/(K_B*T))
    end


    open("spiny_L=$L,T=$T.txt","w") do io

        println(io,S)

        for k in 1:10^6
            for u in 1:L^2
                i = rand(1:L)
                j = rand(1:L)

                E=2*J*S[i,j]*(S[b[i],j]+S[b[i+2],j]+S[i,b[j]]+S[i,b[j+2]])
                E=Int(E)

                if E <= 0
                    S[i,j] = -S[i,j]
                else
                    x = rand()
                    if x < Exp[E+9]
                        S[i,j] = -S[i,j]
                    end
                end
            end

        println(io,S)
        end
    end

end
