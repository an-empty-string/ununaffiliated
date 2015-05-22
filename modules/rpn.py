from modules.commands import command
import operator

@command("rpn", (0, float('inf')))
def rpn(bot, data, args):
    stack = []
    operators = {"+": (operator.add, 2), "-": (operator.sub, 2), "*": (operator.mul, 2), "/": (operator.truediv, 2)}
    for i in args:
        if all(k in "0123456789." for k in i) and i.count(".") <= 1 and ("-" not in i[1:]):
            stack.append(float(i))
        else:
            if i not in operators:
                return bot.say(data["reply_target"], "Unknown operator {}.".format(i))
            opargs = []
            for k in range(operators[i][1]):
                opargs.append(stack.pop())
            stack.append(operators[i][0](*opargs[::-1]))

    bot.say(data["reply_target"], str(stack) if len(stack) > 1 else str(stack[0]))
