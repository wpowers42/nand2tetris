// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// start_pixel = @SCREEN
@SCREEN
D=A
// start_pixel = screen
@start_pixel
M=D
// current_pixel = screen
@current_pixel
M=D
// end_pixel = screen + 8192
@8191 // may have to use 8191
D=D+A
@end_pixel
M=D
@direction
M=1

(LOOP)
    // if (current_pixel < start_pixel) goto RESET_PIXEL_END
    @current_pixel
    D=M
    @start_pixel
    D=D-M
    @RESET_PIXEL_END
    D;JLT
    
    // if (current_pixel > end_pixel) goto RESET_PIXEL_START
    @current_pixel
    D=M
    @end_pixel
    D=D-M
    @RESET_PIXEL_START
    D;JGT
    
    // if (KBD > 0) goto FILL_BLACK
    @KBD
    D=M
    @FILL_BLACK
    D;JGT
    
    // if (KBD = 0) goto FILL_WHITE
    @KBD
    D=M
    @FILL_WHITE
    D;JEQ

    @NEXT_PIXEL
    0;JMP

(NEXT_PIXEL)
    // current_pixel = current_pixel + direction
    @direction
    D=M
    @current_pixel
    M=D+M
    @LOOP
    0;JMP

(FILL_BLACK)
    // set current pixel to black
    @current_pixel
    A=M
    M=-1
    @direction
    M=1
    @NEXT_PIXEL
    0;JMP

(FILL_WHITE)
    // set current pixel to white
    @current_pixel
    A=M
    M=0
    @direction
    M=-1
    @NEXT_PIXEL
    0;JMP

(RESET_PIXEL_START)
    @start_pixel
    D=M
    @current_pixel
    M=D
    @LOOP
    0;JMP

(RESET_PIXEL_END)
    @end_pixel
    D=M
    @current_pixel
    M=D
    @LOOP
    0;JMP