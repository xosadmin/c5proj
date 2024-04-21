import random

requests = [
    "Can you please set up the tent in the designated camping area before dusk?",
    "We need someone to assemble the poles and stake down the corners for the tent.",
    "Could you ensure that the rainfly is properly attached to the tent to protect from potential rain showers?",
    "Please check that all the zippers on the tent are functioning correctly.",
    "It would be great if someone could organize the tent accessories like stakes and guy lines neatly in the provided bag after setup."
    "Can you solve this algebraic equation: 3x + 5 = 20?",
    "What is the perimeter of a rectangle with sides measuring 8 meters and 12 meters?",
    "Calculate the area of a circle with a radius of 6 centimeters.",
    "Find the solution to this quadratic equation: x^2 - 7x + 10 = 0.",
    "A train travels at a speed of 60 miles per hour. How far will it travel in 3 hours?"
]

answers = [
    "To solve the equation 3x + 5 = 20, subtract 5 from both sides first to isolate the term with x. This gives you 3x = 15. Then, divide both sides by 3 to solve for x. So, x = 5.",
    "The perimeter of a rectangle can be calculated using the formula: 2 * (length + width). For a rectangle with sides measuring 8 meters and 12 meters, the perimeter would be 2 * (8 + 12) = 2 * 20 = 40 meters.",
    "The area of a circle can be calculated using the formula: π * radius^2. Given a radius of 6 centimeters, the area would be π * 6^2 = π * 36 ≈ 113.1 square centimeters (rounded to one decimal place).",
    "To find the solutions to the quadratic equation x^2 - 7x + 10 = 0, you can either factor the equation or use the quadratic formula. Factoring the equation gives you (x - 5)(x - 2) = 0. So, the solutions are x = 5 and x = 2.",
    "Distance traveled = Speed * Time. Given a speed of 60 miles per hour and a time of 3 hours, the distance traveled would be 60 * 3 = 180 miles."
]

feelingSentences = [
    "Sometimes, I feel like a ship lost in a vast ocean, unsure of which direction to sail.",
    "When I'm with loved ones, I'm filled with a warmth that spreads through me like sunlight breaking through clouds.",
    "There are moments when I feel a sense of overwhelming gratitude for the simple pleasures life offers.",
    "At times, I wrestle with a deep sense of loneliness, like an echo reverberating in an empty room.",
    "Joy washes over me when I accomplish something I've worked hard for, like reaching the summit of a challenging mountain.",
    "In moments of uncertainty, fear grips my heart like a vice, making it hard to breathe.",
    "The weight of sadness settles on my shoulders like a heavy cloak, enveloping me in its somber embrace.",
    "When I'm in nature, I feel a profound sense of peace and connection, as if I'm a part of something much greater.",
    "Anger bubbles up within me like a simmering pot, fueled by injustice and frustration.",
    "Love fills me with a sense of purpose and belonging, like finding the missing piece of a puzzle that completes me."
]

requestLens = len(requests)
answerLens = len(answers)
feelingLens = len(feelingSentences)

def llmRequests():
    questionNum = random.randint(0,requestLens-1)
    return requests[questionNum]

def llmAnswers():
    answerNum = random.randint(0,answerLens-1)
    return requests[answerNum]

def llmFeelings():
    feelNum = random.randint(0,feelingLens-1)
    return feelingSentences[feelNum]
