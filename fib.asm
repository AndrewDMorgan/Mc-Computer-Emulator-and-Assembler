.Start
    LodI 1 <2>    ; loading a one for to be used (since the alu doesn't have ++ & --)
    LodI 5 <3>    ; the current index of the list
    LodI 0 <4>    ; loading a zero into the first value
    LodI 1 <5>    ; loading a one into the second value
.Loop
        ; generating the next value
    Sub <3> <2> ACC  ; getting the previous value's address
    WrtB ACC         ; loading the previous value's address
    WrtA <3>         ; getting the current value
    Add <0> <0> ACC  ; adding the current two values
    Add <3> <2> <3>  ; getting the next values address and saving it
    WrtW <3>         ; setting the write address of the next spot
    Wrte ACC <0>     ; saving that value

        ; outputing the value and looping
    Outp ACC         ; outputing the new value
    WrtB <3>         ; getting the address of the new value
    LodI 233 ACC     ; loading the max value to the accumulator
    JmpG <0> Loop    ; jumping to the start of the list if the value is smaller then the max value
.LoopExit
    END  ; ending the program
