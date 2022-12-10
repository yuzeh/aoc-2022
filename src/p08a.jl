acc_ud(fn, xs) = accumulate(fn, xs, dims=1)
acc_lr(fn, xs) = accumulate(fn, xs, dims=2)
rev_ud(xs) = reverse(xs, dims=1)
rev_lr(xs) = reverse(xs, dims=2)

function main(filename)
    treeheights = parse(filename)

    # only the center rows can be hidden, so let's figure out which ones they are
    center  = treeheights[2 : end - 1, 2 : end - 1]

    top     = acc_ud(max, treeheights                   )[1 : end - 2, 2 : end - 1]
    bottom  = rev_ud(acc_ud(max, rev_ud(treeheights))   )[3 : end    , 2 : end - 1]
    left    = acc_lr(max, treeheights                   )[2 : end - 1, 1 : end - 2]
    right   = rev_lr(acc_lr(max, rev_lr(treeheights))   )[2 : end - 1, 3 : end    ]

    hidden = (center .<= top) .&& (center .<= bottom) .&& (center .<= left) .&& (center .<= right)

    nvisible = prod(size(treeheights)) - sum(hidden)
    println(nvisible)
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