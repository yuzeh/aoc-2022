# R (vectorized style)
# To run: `Rscript src/p01b.r <filename>`

main = function (filename, n) {
    fd = file(filename, "r")

    pack_weights = strtoi(readLines(fd))
    pack_sum_indexes = is.na(pack_weights)

    pack_weights[pack_sum_indexes] <- 0
    elf_weights_cumsum = cumsum(pack_weights)[pack_sum_indexes]
    elf_weights = c(elf_weights_cumsum[1], diff(elf_weights_cumsum))

    top_n_elf_weights = head(sort(elf_weights, decreasing = TRUE), n)

    print(sum(top_n_elf_weights))
    
    close(fd)
}

main(commandArgs(trailingOnly = TRUE)[1], 3)