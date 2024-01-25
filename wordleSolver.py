import math
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time





#Set up for web scraping
def scrape_wordle():
    url = "https://www.nytimes.com/games/wordle/index.html"
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    try:
        driver.get(url)
        print("Login")
        click_button(driver.find_element(By.CLASS_NAME,'Welcome-module_button__ZG0Zh'), driver)
        print("Close")
        click_button(driver.find_element(By.CLASS_NAME,'Modal-module_closeIcon__TcEKb'), driver)

    except Exception as e:
        print(f"Error: {e}")
    return driver

#Function to click buttons
def click_button(element, driver):
        time.sleep(.1)
        if element:
            element.click()
        else:
            driver.quit()


#Type a Guess
def typeWord(word, driver):
    print("----------------------------------------")
    print("NEW GUESS!")
    #print("Guess : " + word)
    for e in word:
        selector = '[data-key="{}"]'.format(e)
        letter = driver.find_element(By.CSS_SELECTOR,str(selector))
        click_button(letter, driver)

#Find the result of the guess
def getPattern(driver, row):
    print("----------------------------------------")
    print("GUESS RESULTS")
    selector = '[aria-label="Row {}"]'.format(row)
    row = driver.find_element(By.CSS_SELECTOR,str(selector))
    letters = row.find_elements(By.CSS_SELECTOR, '[role="img"]')
    pattern = ""
    time.sleep(2)
    for letter in letters:
        status = letter.get_attribute("data-state")
        if "absent" in status : pattern += "0"
        elif "present" in status : pattern += "1"
        else : pattern += "2"
    #print("Result : " + pattern)
    return pattern


#Find right guess by itterating through each word to find the most likely
def findWord(csv):
    print("----------------------------------------")
    print("SEARCHING FOR THE BEST GUESS")
    log_values = {odds: math.log2(1/odds) for odds in [i/2315 for i in range(1, 2316)]}
    numWords = len(csv)
    patterns = genPatterns()
    maxOdds = 0
    maxWord = '';

    if(len(csv) == 1): return csv[0]
    for guess in csv:
        totalOdds = 0
        for pattern in patterns:
            amount = findAmount(pattern, csv, guess, numWords)
            if amount > 0:
                odds = amount / 2315;
                totalOdds += odds * log_values[odds]
        if(totalOdds > maxOdds):
            maxOdds = totalOdds
            maxWord = guess
    #print("Best guess : " + maxWord)
    return maxWord


#Find amount of possibilities for a certain pattern
def findAmount(pattern, csv, guess, numWords):
    count = 0
    guess_set = set(guess)
    for word in csv:
        if word != guess:
            fail = any(
                pattern[i] == "0" and word[i] in guess_set or
                pattern[i] == "1" and (word[i] == guess[i] or word[i] not in guess_set) or
                pattern[i] == "2" and word[i] != guess[i]
                for i in range(5)
            )
            if not fail:
                count += 1
    return count


#Generates patterns of grey yellow green
def genPatterns():
    patterns = []
    for i in range(3):
        for j in range(3):
            for l in range(3):
                for m in range(3):
                    for n in range(3):
                        patterns.append(str(i) + str(j) + str(l) + str(m) + str(n))
    return patterns


#Gen the CSV
def parseCSV():
    with open('words.csv', newline='') as csvfile:
        data = [word for row in csv.reader(csvfile) for word in row]
    return data

#Modify csv after each result guesses
def updateCSV(csv, input, guess):
    print("----------------------------------------")
    print("UPDATING CSV")
    new_csv = []
    for word in csv:
        fail = any(
            input[i] == "0" and guess[i] in word or
            input[i] == "1" and (word[i] == guess[i] or guess[i] not in word) or
            input[i] == "2" and word[i] != guess[i]
            for i in range(5)
        )
        if not fail:
            new_csv.append(word)

    print("New csv")
    print(new_csv)
    return new_csv


#Main function
if __name__ == "__main__":
    None



def runPY():
    driver = scrape_wordle()
    row = 1
    word = 'slate'
    enter = '↵'
    csv = parseCSV()
    round = 1
    pattern="00000"
    patterns = []
    words=[]
    while round != 6:
        typeWord(word + enter, driver)
        pattern = getPattern(driver, row)
        patterns.append(pattern)
        words.append(word)
        if(pattern == '22222'): break
        round += 1
        row += 1
        csv = updateCSV(csv, pattern, word)
        word = findWord(csv)

    print("----------------------------------------")
    print("FOUND THE ANSWER")
    #print("Answer : " + word)
    print(word)
    print(patterns)
    driver.quit()
    return word, patterns, words



