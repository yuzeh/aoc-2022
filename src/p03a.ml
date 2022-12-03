module CharSet = Set.Make(Char) ;;

let rucksack_to_set (rucksack : string) : CharSet.t =
  let rec explode (index : int) (accumulator : CharSet.t) =
    if index < 0
      then accumulator
      else explode (index - 1) (CharSet.add rucksack.[index] accumulator) in
  explode (String.length rucksack - 1) CharSet.empty ;;

let find_rucksack_common_item (rucksack : string) =
  let half_rucksack_length = (String.length rucksack) / 2 in
  let first_half = rucksack_to_set (String.sub rucksack 0 half_rucksack_length) in
  let second_half = rucksack_to_set (String.sub rucksack half_rucksack_length half_rucksack_length) in
  let intersection = CharSet.inter first_half second_half in
  CharSet.choose intersection

let score_item (value : char) : int =
  if 'a' <= value && value <= 'z'
  then (Char.code value) - Char.code('a') + 1
  else (Char.code value) - Char.code('A') + 27


let main filename =
  let ic = open_in filename in
  let rec agg handle score_accumulator =
    try
      let line = input_line handle in
      let common_item = find_rucksack_common_item (String.trim line) in
      let score = score_item common_item in
      agg handle (score_accumulator + score)
    with End_of_file ->
      score_accumulator in
  let total = agg ic 0 in
    close_in ic;
  print_int total;
  print_endline ""

let () = main Sys.argv.(1)