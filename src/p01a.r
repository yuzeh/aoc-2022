# R (imperative style)
# To run: `Rscript src/p01a.r <filename>`

main = function (filename) {
    fd = file(filename, "r")

    heaviest_pack_weight <- -1
    current_pack_weight <- 0

    newpack = function () {
        heaviest_pack_weight <<- max(c(heaviest_pack_weight, current_pack_weight))
        current_pack_weight <<- 0
    }

    while (TRUE) {
        line = readLines(fd, n = 1)

        if (length(line) == 0) {
            break
        }

        item_weight = strtoi(line)
        if (is.na(item_weight)) {
            newpack()
        } else {
            current_pack_weight <- current_pack_weight + item_weight
        }
    }

    newpack()

    close(fd)

    print(heaviest_pack_weight)
}

main(commandArgs(trailingOnly = TRUE)[1])