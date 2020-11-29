def determinePrimary(emotionLevels):
    strongestLevel = -1
    for key in emotionLevels:
        if(emotionLevels[key] > strongestLevel):
            primaryEmotion = key
            strongestLevel = emotionLevels[key]

    return primaryEmotion


def determineEnhanced(eL, primaryEmotion):

    EnhancedEmotion = 'null'
    if(primaryEmotion == 'happy'):
        if(eL['angry'] >= 30 and eL['angry'] >= eL['calm']):
            EnhancedEmotion = 'energetic'
        elif(eL['calm'] >= 30 and eL['calm'] >= eL['angry']):
            EnhancedEmotion = 'content'

    if(primaryEmotion == 'sad'):
        if(eL['angry'] >= 30 and eL['angry'] >= eL['calm']):
            EnhancedEmotion = 'despair'
        elif(eL['calm'] >= 30 and eL['calm'] >= eL['angry']):
            EnhancedEmotion = 'gloomy'

    if(primaryEmotion == 'angry'):
        if(eL['happy'] >= 30 and eL['happy'] >= eL['sad']):
            EnhancedEmotion = 'energetic'
        elif(eL['sad'] >= 30 and eL['sad'] >= eL['happy']):
            EnhancedEmotion = 'despair'

    if(primaryEmotion == 'calm'):
        if(eL['happy'] >= 30 and eL['happy'] >= eL['sad']):
            EnhancedEmotion = 'content'
        elif(eL['sad'] >= 30 and eL['sad'] >= eL['happy']):
            EnhancedEmotion = 'gloomy'

    return EnhancedEmotion
