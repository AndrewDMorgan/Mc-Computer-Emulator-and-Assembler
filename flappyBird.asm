Jump Start     ; jumping to the program's start 

    ; renders a pillar (works as a function) 
.RenderPilar:
        ; loading data 
    Pop <6>          ; getting the return line 
    Pop <22>         ; getting the bottom height 
    Pop <23>         ; getting the top height 
    Pop <24>         ; getting the x position 
    LodI 2 ACC       ; the amount to jump 
    Add <6> ACC <6>  ; finding the return line number 

        ; rendering the bottom pillar 
    .BottomLoop:
        LodI 1 ACC           ; loading the pixel value 
        Plot <24> <22>       ; plotting the pixel 
        Sub <22> <2> <22>    ; going down a tile 
        Wrte <22> ACC        ; loading the height 
        JmpZ BottomExit      ; leaving the loop 
        Jump BottomLoop      ; looping 
.BottomExit:

        ; rendering the top pillar 
    LodI 32 <25>    ; the max height 
    .TopLoop:
        LodI 1 ACC           ; loading the pixel value 
        Plot <24> <23>       ; plotting the pixel 
        Add <23> <2> <23>    ; going up a tile 
        Wrte <23> ACC        ; loading the height 
        JmpE <25> TopExit         ; leaving the loop 
        Jump TopLoop         ; looping 
.TopExit:
    Jump <6>         ; returning 

; =================================================================================== 

    ; the main program 
.Start:
    RefF             ; disabling constant refresh 

    LodI 1 <2>       ; for incrementing 
    LodI 0 <3>       ; x pos 
    LodI 16 <4>      ; y pos 
    LodI 119 <5>     ; w key for jumping 
        ; 6 is free for calculations 
        ; 7-21 are for the pilar positions 
        ; 22-25 are used in RenderPilar 
    LodI 6 <26>;     ; the time till the next pillar 
    LodI 0 <27>      ; the players score 

    ; pillars are every 7 pixels 
    ; every 7 pixels push the last pillars up one slot 
    ; since one slot is free now and the first is gone add one random pilar 
    ; shift the bottom random number 4 times to get 0-16 and the top 5 to get 0-7 (min gap is 7 pixels) 

.Game:
        ; moving the bird 
    Add <2> <3> <3>    ; moving the bird 1 to the right 
    Sub <4> <2> <4>    ; moving the bird one down 

        ; checking for jumping 
    Inpt ACC           ; getting the keys pressed 
    JmpE <5> Jumping   ; checking if the jump key was pressed 
    Jump PostJump      ; no jump 
.Jumping:
    LodI 6 ACC         ; getting the amount being jumped 
    Add <4> ACC <4>    ; moving the jump amount 
.PostJump:

        ; moving the pillars 
    Add <26> <2> <26>   ; adding one to the counter for spawning pillars 
    LodI 7 ACC          ; checking if a pilar should be spawned 
    JmpG <26> NoPillar  ; the pillars are good as is 

        ; moving pillars memory addresses 
    Wrte <10> <7>
    Wrte <11> <8>
    Wrte <12> <9>

    Wrte <13> <10>
    Wrte <14> <11>
    Wrte <15> <12>

    Wrte <16> <13>
    Wrte <17> <14>
    Wrte <18> <15>

    Wrte <19> <16>
    Wrte <20> <17>
    Wrte <21> <18>

        ; spawning a pillar 
    Add <27> <2> <27>   ; increasing the players score 
    LodI 32 <19>        ; the starting x coord 
    
    Rand ACC            ; getting a random number for the bottom height 
    SftR ACC ACC        ; scalling the number to be correct 
    SftR ACC ACC
    SftR ACC ACC
    SftR ACC ACC
    Wrte ACC 21         ; saving the height 

    Rand ACC            ; getting a random number for the top height 
    SftR ACC ACC        ; scalling the number to be correct 
    SftR ACC ACC
    SftR ACC ACC
    SftR ACC ACC
    SftR ACC ACC
    LodI 31 <26>        ; the ceiling height 
    Sub <26> ACC ACC    ; getting the height from the ceiling 
    Wrte ACC 20         ; saving the height 
    LodI 1 <26>         ; resetting the spawn counter 

.NoPillar:
        ; moving the pillars one to the left 
    Sub <7> <2> <7>
    Sub <10> <2> <10>
    Sub <13> <2> <13>
    Sub <16> <2> <16>
    Sub <19> <2> <19>

        ; checking if the bird died 
    Wrte <4> ACC        ; loading the y coord to the accumulator 
    JmpZ Dead           ; killing the bird if at zero 

    ; check collision with the third? pillar 
    Wrte <14> ACC       ; loading the third pillar 
    JmpZ DeathDone      ; making sure there is a valid platform 
    LodI 16 ACC         ; the players x position 
    JmpE <13> Collision ; testing for collision 
    Jump DeathDone      ; the player can't die 
.Collision:
    Wrte <4> ACC        ; loading the y coord to the accumulator 
    JmpL <15> Dead      ; checking if the bird died 
    JmpG <14> Dead      ; checking if the bird died 

.DeathDone:
        ; rendering the pillars 
    Cler                ; clearing the screen 

        ; pillar 1 
    Push <7>            ; pushing the x coord 
    Push <8>            ; pushing the top height 
    Push <9>            ; pushing the bottom height 
    Push <1>            ; pushing the line number 
    Jump RenderPilar    ; calling the function to render them 

        ; pillar 2 
    Push <10>           ; pushing the x coord 
    Push <11>           ; pushing the top height 
    Push <12>           ; pushing the bottom height 
    Push <1>            ; pushing the line number 
    Jump RenderPilar    ; calling the function to render them 

        ; pillar 3 
    Push <13>           ; pushing the x coord 
    Push <14>           ; pushing the top height 
    Push <15>           ; pushing the bottom height 
    Push <1>            ; pushing the line number 
    Jump RenderPilar    ; calling the function to render them 

        ; pillar 4 
    Push <16>           ; pushing the x coord 
    Push <17>           ; pushing the top height 
    Push <18>           ; pushing the bottom height 
    Push <1>            ; pushing the line number 
    Jump RenderPilar    ; calling the function to render them 

        ; pillar 5 
    Push <19>           ; pushing the x coord 
    Push <20>           ; pushing the top height 
    Push <21>           ; pushing the bottom height 
    Push <1>            ; pushing the line number 
    Jump RenderPilar    ; calling the function to render them 

        ; rendering the bird 
    Wrte <2> ACC     ; loading a 1 to the accumulator 
    LodI 16 <6>      ; the center of the screen 
    Plot <6> <4>     ; drawing the bird 
    Refr             ; refreshing the screen 

    Jump Game        ; looping 
.Dead:
    LodI 3 ACC          ; the number of extra spawns before the player has to play 
    Sub <27> ACC ACC    ; correcting for the first spawns 
    Outp ACC            ; outputing the score 
    END                 ; ending the program 

