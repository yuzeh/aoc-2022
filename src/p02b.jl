OUTCOMES = [
    3 6 0
    0 3 6
    6 0 3
]

PLAY_TO_INDEX = Dict(:rock => 1, :paper => 2, :scizzors => 3)
INDEX_TO_PLAY = [:rock :paper :scizzors]
OUTCOME_TO_DIRECTION = Dict(:win => 1, :draw => 0, :lose => -1)
SHAPE_SCORE = Dict(:rock => 1, :paper => 2, :scizzors => 3)

function outcome_score(opponent_play, player_play)
    return OUTCOMES[PLAY_TO_INDEX[opponent_play], PLAY_TO_INDEX[player_play]]
end

function shape_score(opponent_play, player_play)
    return SHAPE_SCORE[player_play]
end

OPPONENT_MAPPING = Dict("A" => :rock, "B" => :paper, "C" => :scizzors)
SELF_MAPPING = Dict("X" => :win, "Y" => :draw, "Z" => :lose)

function main(filename)
    filetext = open(filename) do f
        read(f, String)
    end

    filetokens = split(filetext)

    opponent_plays = map((x) -> OPPONENT_MAPPING[x], filetokens[1:2:end])
    self_outcomes = map((x) -> SELF_MAPPING[x], filetokens[2:2:end])
    self_plays = map((opponent_play, self_outcome) -> INDEX_TO_PLAY[(OUTCOME_TO_DIRECTION[self_outcome] + PLAY_TO_INDEX[opponent_play]) % 3 + 1], opponent_plays, self_outcomes)

    outcome_scores = map(outcome_score, opponent_plays, self_plays)
    shape_scores = map(shape_score, opponent_plays, self_plays)

    println(sum(outcome_scores + shape_scores))
end

main(ARGS[1])
