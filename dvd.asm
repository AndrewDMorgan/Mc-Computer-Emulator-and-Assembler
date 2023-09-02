Jump Start    ; jumping to the programs start because I put the function in a terrible spot 

        ; flips a value from 1-2 to the opposite (for directions), is formated as a function call to test stuff (is completly redudent, could be replaced with one LodI) 
.Flip:
    Pop <9>             ; getting the line number to jump to 
    Pop <10>            ; getting the value being flipped 
    LodI 3 ACC          ; 3 - (1-2) = the opposite 
    SubL <10> ACC ACC   ; flipping the value 
    Push ACC            ; pushing the results onto the stack 
    LodI 2 ACC          ; used to increment by two to pass the call point 
    Add <9> ACC <9>     ; jumping to the line after the call 
    Jump <9>            ; jumping back to the line where the program is from 

            ; the main program 

.Start:
    LodI 1 <2>    ; x 
    LodI 1 <3>    ; y 
    LodI 2 <4>    ; x velocity 
    LodI 1 <5>    ; y velocity 
    LodI 2 <6>    ; direction x 
    LodI 2 <7>    ; direction y 
    LodI 0 <8>    ; loop counter 
    RefF          ; setting constant refresh to false 
.Loop:
    LodI 1 ACC         ; loading a one to the accumulator 
    Add ACC <8> <8>    ; adding one to the counter 

        ; moving the point 

    LodI 1 ACC            ; for comparing the directions 
    JmpE <6> NegativeX    ; checking the x direction 
    Add <2> <4> <2>       ; moving it right 
    Jump EndX             ; jumping past the left movement 
.NegativeX:
    Sub <2> <4> <2>       ; moving it on the x axis 
.EndX:
    JmpE <7> NegativeY    ; checking the y direction 
    Add <3> <5> <3>       ; moving it up 
    Jump EndY             ; jumping past the downward movement 
.NegativeY:
    Sub <3> <5> <3>       ; moving it down 
.EndY:

        ; handling left wall colision 
    
    Wrte <2> ACC     ; the x value 
    JmpZ Left        ; checking if the value is off the screen 
    Jump LeftEnd     ; continuing because no collision happened 
.Left:
    Push <6>         ; pushing the x velocity 
    Push <1>         ; pushing the line number 
    Jump Flip        ; flipping the x velocity 
    Pop <6>          ; getting the flipped value back 
    LodI 1 ACC       ; loading a 1 to the acc 
    Wrte ACC <2>     ; setting the x to 1 (so it's not out of range) 
.LeftEnd:

        ; handling right wall colision 

    LodI 32 ACC          ; loading a 32 into the accumulator 
    JmpG <2> RightEnd    ; checking if the value is too large 

    Push <6>         ; pushing the x velocity 
    Push <1>         ; pushing the line number 
    Jump Flip        ; flipping the x velocity 
    Pop <6>          ; getting the flipped value back 
    LodI 31 ACC      ; loading a 31 to the acc 
    Wrte ACC <2>     ; setting the x to 31 (so it's not out of range) 
.RightEnd:

        ; handling bottom wall colision 

    Wrte <3> ACC     ; the y value 
    JmpZ Bottom      ; checking if the value is off the screen 
    Jump BottomEnd   ; continuing because no collision happened 
.Bottom:
    Push <7>         ; pushing the y velocity 
    Push <1>         ; pushing the line number 
    Jump Flip        ; flipping the y velocity 
    Pop <7>          ; getting the flipped value back 
    LodI 1 ACC       ; loading a 1 to the acc 
    Wrte ACC <3>     ; setting the y to 1 (so it's not out of range) 
.BottomEnd:

        ; handling top wall colision 

    LodI 32 ACC        ; loading a 32 into the accumulator 
    JmpG <3> TopEnd    ; checking if the value is too large 

    Push <7>         ; pushing the y velocity 
    Push <1>         ; pushing the line number 
    Jump Flip        ; flipping the y velocity 
    Pop <7>          ; getting the flipped value back 
    LodI 31 ACC      ; loading a 31 to the acc 
    Wrte ACC <3>     ; setting the y to 31 (so it's not out of range) 
.TopEnd:

        ; plotting the point 

    LodI 0 ACC         ; setting the pixel color to blank 
    Cler               ; clearing the screen 
    LodI 1 ACC         ; setting the pixel color to on 
    Plot <2> <3>       ; plotting the point 
    Refr               ; refreshing the screen 
    LodI 20 ACC        ; loading the max itteration value 
    JmpG <8> Loop      ; looping 
.End:
    END    ; ending the program 
