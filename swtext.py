import pygame

def scroll_text_with_vanishing_point(text, font_name, start_font_size, font_color, surface, speed=1):
    """
    Scrolls the given text across the screen with a vanishing point effect.

    Args:
    - text (str): The large text string to display.
    - font_name (str): The name of the font (or a font file path) to use for rendering text.
    - start_font_size (int): The initial font size to start with.
    - font_color (tuple): The font color as an RGB tuple.
    - surface (pygame.Surface): The pygame surface (e.g., screen) to render text on.
    - speed (float): The speed at which the text scrolls.
    """

    # Split text into lines that fit within the surface width
    def break_text_into_lines(text, font, surface_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_width, _ = font.size(test_line)
            if text_width > surface_width or word == "\n":
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        return lines
    
    # Set up the initial font and break the text into lines
    font = pygame.font.Font(font_name, start_font_size)
    lines = break_text_into_lines(text, font, surface.get_width())
    
    # Reverse the lines so that they start from the top of the screen
    lines.reverse()

    # Initial position of the text on the surface (off-screen initially)
    #y_position = surface.get_height() + 50  # Start just below the screen

    # Scroll the text upward while reducing the font size for the vanishing point effect
    running = True
    clock = pygame.time.Clock()
    
    # Adjust vertical space for the lines to avoid overlap
    line_spacing = 20  # Space between lines, added to avoid overlap

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to trigger the scroll
                    y_position = surface.get_height() + len(lines) * ((start_font_size * 1.23) + line_spacing) # Reset text position to start scrolling
                    scroll_text(surface, lines, font_name, start_font_size, font_color, y_position, line_spacing)
                    running = False  # End after the click triggers the scroll

        # Draw button to start scrolling
        surface.fill((0, 0, 0))  # Clear screen
        font = pygame.font.Font(font_name, 30)
        button_text = font.render("Click to Start Scrolling", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(button_text, button_rect)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

def scroll_text(surface, lines, font_name, start_font_size, font_color, y_position, line_spacing):
    """
    Actual scrolling of the text across the screen with a vanishing point effect.
    """

    font = pygame.font.Font(font_name, start_font_size)
    running = True
    clock = pygame.time.Clock()

    # Adjust vertical space for the lines to avoid overlap
    line_spacing = 20  # Space between lines, added to avoid overlap
    firstl = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen with a black background
        surface.fill((0, 0, 0))
        
        # Draw each line of text, with increasing vertical offset and decreasing font size
        line_y_position = y_position
        for i, line in enumerate(lines):
            # Calculate the shrinking effect based on the line's position
            distance_from_top = surface.get_height() - line_y_position  # Distance from the top of the screen

            # Prevent negative values and safely compute the shrink factor
            shrink_factor = max(0, distance_from_top / surface.get_height())

            # Create the font surface normally at the starting font size

            font = pygame.font.Font(font_name, start_font_size)
            text_surface = font.render(line, True, font_color)

            # Scale the text surface based on the shrink factor
            scale_factor = 1 - shrink_factor * 0.7  # You can adjust the 0.7 factor for different scaling effects
            new_width = int(text_surface.get_width() * scale_factor)
            new_height = int(text_surface.get_height() * scale_factor)
            scaled_text_surface = pygame.transform.scale(text_surface, (new_width, new_height))

            # Calculate the position of the text
            text_rect = scaled_text_surface.get_rect(center=(surface.get_width() // 2, line_y_position))

            # Blit the scaled text to the screen
            surface.blit(scaled_text_surface, text_rect)

            # Adjust vertical position for the next line
            line_y_position -= new_height + line_spacing  # Adjust vertical spacing based on scaled height
            # Remove lines that are no longer visible (within 20% of the top of the screen)
            if line_y_position <= surface.get_height() * 0.2:
                firstl = False
                lines.pop(i)

        
        # Move the entire block of text up the screen
        y_position -= 3  # Speed of scrolling (slower than before)
        if y_position + len(lines) * (start_font_size + line_spacing) < 0:
            running = False  # Stop when the text is off-screen
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

# --- Example usage ---
if __name__ == "__main__":
    pygame.init()

    # Set up the screen
    screen_width = 1600
    screen_height = 840
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Vanishing Point Text Effect")

    # Define text, font, color
    text = """Assault Shark 
    \n \n The year is 2317, and the battleground has spread, not just beneath the waves, but high above in the skies.
    \n \n Science’s attempts to control nature have led to the creation of the ultimate weapon: bio-engineered creatures designed to fight in the most unforgiving of environments. 
    \n \n The most feared of them all? You. 
    \n \n The last surviving free eggheads, guardians of the fading spark of mankind's learning, eke out a precarious survival on near-orbit asteroid stations.  To regain Earth, they have plotted a dangerous mission. \n \n
    \n \n You must return to the skies, and strike down the evil mutant exo-marine jet creatures. Rescue more eggheads, reclaim the ancient fortresses of wisdom, and save Earth for a new age of enlightenment.
    \n \n You are the Shark Knight, the last remaining knight of the mystical order: pilots of jet-powered, bio-mechanical shark aircraft - a lethal fusion of oceanic predator and cutting-edge technology.  With advanced weaponry, agile jet propulsion, and the instincts of a true apex predator, you are the future's final hope against the plague of evil bio-craft.
    \n \n The skies are filled with deadly creatures: mutated squidships, transgenic manta blimps, rocket fish, and other monstrosities, each vying for dominion over the oceans and skies alike.  Supported by the artillery of the cryptofacist groundlings, the atmosphere has long been viewed as an impregnable death zone.
    \n \n Your mission: fight, survive, and conquer. Only one can rule the skies, and it’s time for the world to remember why the Shark is the ultimate predator.
    \n \n Out there, they’ll fear your bite.
    \n \n Welcome to the Assault Shark.
    \n \n Prepare for battle."""
    
    font_name = "fonts/arcade_r.ttf" # Use system font or provide a font path
    start_font_size = 60
    font_color = (255, 255, 0)  # Yellow color

    # Call the function to scroll the text
    scroll_text_with_vanishing_point(text, font_name, start_font_size, font_color, screen)

    # Quit Pygame
    pygame.quit()