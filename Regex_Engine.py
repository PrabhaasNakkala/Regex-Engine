

def characters(regex, word, word_ptr):                                                  #   Matches characters and updates word pointer 
    chars = []
    i = 0
    answer = True

    while i < len(regex):                                                               #   Splits string by curly brackets and operators and slashes
        if regex[i] == '{':
            chars[-1] = chars[-1] + regex[i:regex.find('}', i) + 1]
            i = regex.find('}', i)
        elif regex[i] == '*' or regex[i] == '+' or regex[i] == '?':
            chars[-1] += regex[i]
        elif regex[i - 1] == '\\':
            chars[-1] += regex[i]
        else: 
            chars.append(regex[i])
        i += 1
    x = 0

    while x < len(chars) and word_ptr <= len(word):

        if '{' in chars[x]:                                                                     #   Accounts for characters next to curly brackets
            [answer, word_ptr] = curly_brackets(chars[x][1:], word, word_ptr, chars[x][0])
            if answer == False: 
                break
            x += 1
        elif chars[x][-1] == '*':
            if word_ptr != len(word):
                if chars[x][0] != word[word_ptr]:
                    x += 1
                    continue
                while chars[x][0] == word[word_ptr]:                         
                    word_ptr += 1
                    if word_ptr == len(word): 
                        break
            x += 1
        elif chars[x][-1] == '+':
            if word_ptr != len(word):
                if word[word_ptr] != chars[x][0]:
                    answer = False
                    break
                else:
                    while chars[x][0] == word[word_ptr]:
                        word_ptr += 1
                        if word_ptr == len(word):
                            break
                    x+=1
                    if word_ptr == len(word):
                        break
            else: 
                answer = False
                break
        elif chars[x][-1] == '?':
            if word_ptr != len(word):
                if word[word_ptr] == chars[x][0]:
                    word_ptr += 1
            x+=1
        elif chars[x] == '.':
            x += 1
            word_ptr += 1
        elif chars[x][0] == '\\':
            if chars[x][1] == 'd':
                if word[word_ptr] <= '9':
                    word_ptr += 1
                    x += 1
                else:
                    answer = False
                    break
            elif chars[x][1] == 'w':
                if word[word_ptr] <= '9' or word[word_ptr].isalpha() or word[word_ptr] == '_':
                    word_ptr += 1
                    x += 1
                else:
                    answer = False
                    break
            else:            
                word_ptr += 1
                x += 1
        elif word[word_ptr] != chars[x]:
            answer = False
            x += 1
            break 
        else: 
            if chars[x] == word[word_ptr]:
                word_ptr += 1
                x += 1
        if word_ptr == len(word) and x != len(chars) and chars[-1].find('*') == False and chars[-1].find('?') == False and word[word_ptr - 1].isalpha():
            answer = False
            break

    return [answer, word_ptr]


def curly_brackets(regex, word, word_ptr, chars):                                   #   matches values with curly brackets and returns word pointer
    
    val1 = int(regex[regex.find('{')+1])
    answer = True
    word = word + ' '

    if regex[regex.find('}')-1].isdigit() and regex[regex.find('}')-2] == ',':
        val2 =  regex[regex.find('}')-1]
        x = 0
        while x < int(val2) and word[word_ptr] in chars:
            word_ptr += 1
            x += 1
        if x < val1:
            answer = False

    if regex[regex.find('}')-1] == ',':
        x = 0 
        while word[word_ptr] in chars:
            word_ptr += 1
            x += 1
        if x < val1:
            answer = False

    if regex.find('}') - regex.find('{') == 2:
        x = 0
        while x < val1 and word[word_ptr] in chars:
            word_ptr += 1
            x += 1
        if x != val1:
            answer = False   
            
    return [answer, word_ptr]


def brackets(regex, word, word_ptr):                                #   matches values in brackets, increments by operator and returns word pointer
    
    chars = []
    i = 1
    answer = True

    while i < regex.find(']'):
        if(regex[i+1] != '-'):      
            chars.append(regex[i])
        elif regex[i].isalpha() and regex[i+1] == '-':
            j = ord(regex[i])
            while j <= ord(regex[i + 2]):
                chars.append(chr(j))
                j += 1
            i += 2
        elif regex[i].isdigit() and regex[i+1] == '-':
            j = int(regex[i])
            while j <= int(regex[i+2]):
                chars.append(str(j))
                j += 1
            i += 2
        i += 1
    word = word + ' '

    if regex[-1] == '+':
        if word[word_ptr] not in chars:
            answer = False
        else: 
            while word[word_ptr] in chars:
                word_ptr += 1
    elif regex[-1] == '?':
        if word[word_ptr] in chars:
            word_ptr += 1
    
    elif regex[-1] == '*':
        while word[word_ptr] in chars:
            word_ptr += 1
    elif '{' in regex:
        return curly_brackets(regex, word, word_ptr, chars)
    else:
        if word[word_ptr] in chars: 
            word_ptr += 1
        else: answer = False

    return [answer, word_ptr]


def parentheses(regex, word, word_ptr):                 #   matches values in parentheses, increments by operator and returns word pointer
    answer = True

    if regex[-1] == '*':                                                                                                
        while len(word) - word_ptr - 1 >= len(regex[1:regex.find(')')]) and answer:
            [answer, word_ptr] = characters(regex[1:regex.find(')')], word, word_ptr)
        answer = True
        return [answer, word_ptr]

    elif regex[-1] == '+':
        if len(word) - word_ptr - 1 >= len(regex[1:regex.find(')')]) and answer:
            while len(word) - word_ptr - 1 >= len(regex[1:regex.find(')')]) and answer:
                [answer, word_ptr] = characters(regex[1:regex.find(')')], word, word_ptr)
            answer = True
            return [answer, word_ptr]
        else: 
            answer = False
            return [answer, word_ptr]
    elif regex[-1] == '?':
        if len(word) - word_ptr - 1 >= len(regex[1:regex.find(')')]) and answer:
            temp = word_ptr
            [answer, word_ptr] = characters(regex[1:regex.find(')')], word, word_ptr)
            if answer:
                return [True, word_ptr]
            else:
                return [True, temp]
        else: 
            answer = True
            return [answer, word_ptr]

    [answer, word_ptr] = characters(regex, word, word_ptr)
    return [answer, word_ptr]

def split(term):                                                                        #   Splits string based on brackets and operators
    list = []
    i = 0

    while i < len(term):
        if term[i].isalpha() or term[i].isdigit() or term[i] == '.':
            if i == 0: 
                list.append(term[i])
            else:
                if term[i-1].isalpha() or term[i-1].isdigit() or term[i-1] == '|':
                    list[-1] = list[-1] + term[i]
                else:
                    list.append(term[i])
            i += 1
        elif term[i] == '[':
            list.append(term[i:term.find(']', i) + 1])
            i = term.find(']', i) + 1
        elif term[i] == '{':
            list[-1] = list[-1] + term[i:term.find('}', i)+1]
            i = term.find('}', i) + 1
        elif term[i] == '(':
            list.append(term[i:term.find(')', i) + 1])
            i = term.find(')', i) + 1
        elif term[i] == '*' or term[i] == '+' or term[i] == '?':
            list[-1] = list[-1] + term[i]
            i += 1
        elif term[i] == '\\':
            list.append(term[i] + term[i+1])
            i+= 2
        
    return list

             
def match(regex, word):                                                         #   Matches expression and word and returns if true or false
    
    word_ptr = 0
    i = 0
    list = split(regex)
    answer = True
    
    for i in range(0, len(list)):
        if list[i][0] == '[':
            answer = True
            [answer, word_ptr] = brackets(list[i], word, word_ptr)
            if answer == False: return False
        if list[i][0] == '(':
            answer = True
            [answer, word_ptr] = parentheses(list[i], word, word_ptr)
            if answer == False: return False
        if list[i][0].isalpha() or list[i][0] == '\\':
            answer = True
            [answer, word_ptr] = characters(list[i], word, word_ptr)
            if answer == False: return False
        if word_ptr < len(word):
            answer = False
    return answer

def main():
    regex = input(r'Enter Regular Expression: ')
    word = input(r'Enter Word: ')
    matched = match(regex, word)
    print(matched)

if __name__ == '__main__':
    main()
    