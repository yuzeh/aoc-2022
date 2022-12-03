PLAY_TO_INDEX = Dict(:rock => 1, :paper => 2, :scizzors => 3)
INDEX_TO_PLAY = [:rock :paper :scizzors]
SHAPE_SCORE = Dict(:rock => 1, :paper => 2, :scizzors => 3)
OUTCOME_SCORE = Dict(:win => 6, :draw => 3, :lose => 0)

function outcome(opponent_play, player_play)
    result_indicator = (PLAY_TO_INDEX[player_play] - PLAY_TO_INDEX[opponent_play] + 3) % 3
    if result_indicator == 0
        return :draw
    elseif result_indicator == 1
        return :win
    else
        return :lose
    end
end

function deduce_play(opponent_play, player_outcome)
    for player_play in INDEX_TO_PLAY
        if outcome(opponent_play, player_play) == player_outcome
            return player_play
        end
    end
    throw(InvalidStateException("Could not find correct play for player outcome"))
end

@assert outcome(:rock, :paper) == :win
@assert outcome(:rock, :rock) == :draw
@assert outcome(:rock, :scizzors) == :lose

OPPONENT_MAPPING = Dict("A" => :rock, "B" => :paper, "C" => :scizzors)
SELF_MAPPING = Dict("X" => :lose, "Y" => :draw, "Z" => :win)

function main(filename)
    filetext = open(filename) do f
        read(f, String)
    end

    filetokens = split(filetext)

    opponent_plays = map((x) -> OPPONENT_MAPPING[x], filetokens[1:2:end])
    self_outcomes = map((x) -> SELF_MAPPING[x], filetokens[2:2:end])
    self_plays = map(deduce_play, opponent_plays, self_outcomes)
    outcome_scores = map((x) -> OUTCOME_SCORE[x], self_outcomes)
    shape_scores = map((x) -> SHAPE_SCORE[x], self_plays)

    println(sum(outcome_scores + shape_scores))
end

main(ARGS[1])
