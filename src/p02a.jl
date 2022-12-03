function outcome_score(opponent_play, player_play)
    if opponent_play == "rock" && player_play == "rock"
        return 3
    elseif opponent_play == "rock" && player_play == "paper"
        return 6
    elseif opponent_play == "rock" && player_play == "scizzors"
        return 0
    elseif opponent_play == "paper" && player_play == "rock"
        return 0
    elseif opponent_play == "paper" && player_play == "paper"
        return 3
    elseif opponent_play == "paper" && player_play == "scizzors"
        return 6
    elseif opponent_play == "scizzors" && player_play == "rock"
        return 6
    elseif opponent_play == "scizzors" && player_play == "paper"
        return 0
    elseif opponent_play == "scizzors" && player_play == "scizzors"
        return 3
    else
        throw(InvalidStateException("Invalid play: opponent_play=$opponent_play player_play=$player_play"))
    end
end

function shape_score(opponent_play, player_play)
    if player_play == "rock"
        return 1
    elseif player_play == "paper"
        return 2
    elseif player_play == "scizzors"
        return 3
    else
        throw(InvalidStateException("Invalid play: opponent_play=$opponent_play player_play=$player_play"))
    end
end

OPPONENT_MAPPING = Dict("A" => "rock", "B" => "paper", "C" => "scizzors")
SELF_MAPPING = Dict("X" => "rock", "Y" => "paper", "Z" => "scizzors")

function main(filename)
    filetext = open(filename) do f
        read(f, String)
    end

    filetokens = split(filetext)

    opponent_plays = map((x) -> OPPONENT_MAPPING[x], filetokens[1:2:end])
    self_plays = map((x) -> SELF_MAPPING[x], filetokens[2:2:end])

    outcome_scores = map(outcome_score, opponent_plays, self_plays)
    shape_scores = map(shape_score, opponent_plays, self_plays)

    println(sum(outcome_scores + shape_scores))
end

main(ARGS[1])
