acc_ud(fn, xs) = accumulate(fn, xs, dims=1)
acc_lr(fn, xs) = accumulate(fn, xs, dims=2)
rev_ud(xs) = reverse(xs, dims=1)
rev_lr(xs) = reverse(xs, dims=2)

function main(filename)
    treeheights = parse(filename)
    h, w = size(treeheights)

    function top(i, j)
        count = 0
        ii = i - 1
        while ii > 0
            count += 1
            if treeheights[ii, j] >= treeheights[i, j]
                break
            end
            ii -= 1
        end
        return count
    end

    function bottom(i, j)
        count = 0
        ii = i + 1
        while ii <= h
            count += 1
            if treeheights[ii, j] >= treeheights[i, j]
                break
            end
            ii += 1
        end
        return count
    end

    function left(i, j)
        count = 0
        jj = j - 1
        while jj > 0
            count += 1
            if treeheights[i, jj] >= treeheights[i, j]
                break
            end
            jj -= 1
        end
        return count
    end

    function right(i, j)
        count = 0
        jj = j + 1
        while jj <= w
            count += 1
            if treeheights[i, jj] >= treeheights[i, j]
                break
            end
            jj += 1
        end
        return count
    end

    # only the center rows can be hidden, so let's figure out which ones they are
    tops    = [   top(i, j) for i in 1:h, j in 1:w]
    bottoms = [bottom(i, j) for i in 1:h, j in 1:w]
    lefts   = [  left(i, j) for i in 1:h, j in 1:w]
    rights  = [ right(i, j) for i in 1:h, j in 1:w]

    println(maximum(tops .* bottoms .* lefts .* rights))
end

function parse(filename)
    filetext = open(filename) do f
        read(f, String)
    end

    filelines = split(filetext)
    treeheights_char = reduce(vcat, (permutedims(collect(s)) for s in filelines))
    return map(Int, treeheights_char) .- Int('0')
end

main(ARGS[1])