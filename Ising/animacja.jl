using Plots

anim(T,L) = begin

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
    heatmap(S,c=:blues,colorbar=false,title="Spiny L=$L, T=$T")


    anim = @animate for i=1:2*10^3

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
        a=S[1,1]
        S[1,1]=1
        heatmap(S,c=:blues,colorbar=false,title="Spiny L=$L, T=$T")
        S[1,1]=a

    end

    gif(anim, "spinyL=$L,T=$T.gif", fps=50)


end
