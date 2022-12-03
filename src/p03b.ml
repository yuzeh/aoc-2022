module CharSet = Set.Make(Char) ;;

let rucksack_to_set (rucksack : string) : CharSet.t =
  let rec explode (index : int) (accumulator : CharSet.t) =
    if index < 0
      then accumulator
      else explode (index - 1) (CharSet.add rucksack.[index] accumulator) in
  explode (String.length rucksack - 1) CharSet.empty ;;

let score_item (value : char) : int =
  if 'a' <= value && value <= 'z'
  then (Char.code value) - Char.code('a') + 1
  else (Char.code value) - Char.code('A') + 27

let main filename =
  let ic = open_in filename in
  let read_rucksack handle = handle
    |> input_line
    |> String.trim
    |> rucksack_to_set in
  let rec score_aggregate score_accumulator =
    try
      let rucksack_set_1 = read_rucksack ic in
      let rucksack_set_2 = read_rucksack ic in
      let rucksack_set_3 = read_rucksack ic in
      let common_item = rucksack_set_1
        |> CharSet.inter rucksack_set_2
        |> CharSet.inter rucksack_set_3
        |> CharSet.choose in
      let score = score_item common_item in
      score_aggregate (score_accumulator + score)
    with End_of_file ->
      score_accumulator in
  let total = score_aggregate 0 in
  close_in ic;
  print_int total;
  print_endline ""

let () = main Sys.argv.(1)