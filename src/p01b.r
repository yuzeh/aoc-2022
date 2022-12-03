# R (vectorized style)
# To run: `Rscript src/p01b.r <filename>`

main <- function(filename, n) {
    fd <- file(filename, "r")

    # The empty strings get turned into NAs so `pack_weights` looks like:
    #   [1000, 2000, 3000, NA,
    #    4000, NA,
    #    5000, 6000, NA,
    #    (etc...)]
    pack_weights <- strtoi(readLines(fd))
    if (!is.na(pack_weights[length(pack_weights)])) {
        # Make sure every elf's set of packs ends with an NA.
        pack_weights <- c(pack_weights, NA)
    }
    pack_sum_indexes <- is.na(pack_weights)

    # The next step is to do a cumsum on the array, treating NAs as 0.
    # The result of that looks like:
    #   [1000, 3000, 6000, <6000>,
    #    10000, <10000>,
    #    15000, 21000, <21000>,
    #    (etc...)]
    # Emphasis added to the positions that were previously NA, because those
    # store important information needed to recover each elf's weight total.
    pack_weights[pack_sum_indexes] <- 0
    pack_weights_cumsum <- cumsum(pack_weights)

    # The result of the following looks like:
    #   [6000, 10000, 21000, (etc...)]
    # (Those weights are a cumsum of the weight total for each elf.)
    elf_weights_cumsum <- pack_weights_cumsum[pack_sum_indexes]

    # To recover the individual elf weight totals, we can use the
    # differencing function.
    # The result looks like:
    #   [6000, 4000, 11000, (etc...)]
    elf_weights <- diff(c(0, elf_weights_cumsum))

    # Finally, take the top N and then sum.
    top_n_elf_weights <- head(sort(elf_weights, decreasing = TRUE), n)
    print(sum(top_n_elf_weights))

    close(fd)
}

main(commandArgs(trailingOnly = TRUE)[1], 3)
