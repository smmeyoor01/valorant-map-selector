from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

#include
import scraping_helpers

def scrape_match_data(driver, base_url):
    
    # Get the map IDs
    map_ids = scraping_helpers.get_map_ids(driver)
    # Initialize a list to hold the data for each map
    match_data = []
    
    for i, map_id in enumerate(map_ids):
        try:
            # Load map-specific data
            driver.get(f'{base_url}/?game={map_id}&tab=overview')
            
            # Get map name
            map_name = get_map(driver)
            
            # Get total scores
            try:
                total_scores = get_total_scores(driver)
            except Exception as e:
                print(e)
            
            # Get half scores for CT and T sides
            ct_scores = get_half_scores(driver, 'ct')
            t_scores = get_half_scores(driver, 't')

            # Get agent names for the current map
            agents = get_agents(driver, i + 1)  # Map numbers are 1-indexed
            # Split agents into two teams (assuming 5 agents per team)
            team1_agents = agents[:5]
            team2_agents = agents[5:]
            
            # Store data for each team separately
            team1_data = {
                'team': 'Team 1',
                'total_score': total_scores[0],
                'ct_score': ct_scores[0],
                't_score': t_scores[0],
                'agents': team1_agents
            }
            
            team2_data = {
                'team': 'Team 2',
                'total_score': total_scores[1],
                'ct_score': ct_scores[1],
                't_score': t_scores[1],
                'agents': team2_agents
            }
            
            # Store all the data in a dictionary for this map
            map_data = {
                'map_id': map_id,
                'map_name': map_name,
                'teams': [team1_data, team2_data]
            }
            
            # Add the map data to the match data
            match_data.append(map_data)
        except Exception as e:
            print(f"Skipping due to error: {e}")
            continue
    return match_data


def get_map(driver):
    map_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="map"]/div[1]/span')))
    for element in map_elements:
        map_name = element.text
        if map_name != "":
            return map_name.strip("PICK").strip()

def get_total_scores(driver):
    map_elements = driver.find_elements(By.CLASS_NAME, 'score')
    test = []
    for element in map_elements:
        if element.text == "":
            continue
        test.append(int(element.text))
    return test

def get_half_scores(driver, side):
    side_definitions = {'ct': "mod-ct", 't': "mod-t"}
    map_elements = driver.find_elements(By.XPATH, f'//span[@class="{side_definitions[side]}"]')
    test = []
    for element in map_elements:
        if element.text != '':
            test.append(int(element.text))
    return test

def get_agents(driver, map_number):
    # Dynamically determine map range based on length of map_elements
    map_elements = driver.find_elements(By.XPATH, '//td[@class="mod-agents"]/div/span[1]/img')
    # Calculate the number of agents per map (assuming 10 agents per map)
    agents_per_map = 10
    num_maps = len(map_elements) // agents_per_map
    
     # # Check if the requested map_number is within the valid range
    if map_number < 1 or map_number > num_maps:
          raise ValueError(f"Invalid map number. Please provide a map number between 1 and {num_maps}.")
    
    # # Calculate the starting and ending index for the given map
    start_idx = (map_number - 1) * agents_per_map
    end_idx = start_idx + agents_per_map
    
    # # Extract agent names using the helper function
    agent_names = [scraping_helpers.agent_name(element.get_attribute('src')) for element in map_elements]
    return agent_names[start_idx:end_idx]