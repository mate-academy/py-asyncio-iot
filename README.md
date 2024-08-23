n# Python Asyncio IoT

**Please note:** read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md)
before starting.

You're given a skeleton of the IoT service taken from the internet. 
As you have noticed — it's fully synchronous and has blocking operations (for example, sleep). 
This task aims to make the program work faster (using `asyncio`) without breaking its logic.

For easier asynchronous setup, please follow these steps:
1. Make your code use `asyncio` - `connect`/`disconnect`/`send_message` must be async functions (just the `async`/`await` interface). 
   Is the code working faster? If the answer is no - then proceed.
2. Try to `gather` registering devices — that should be easy. Devices may be registered **simultaneously**.
   And when you run the code — wow, it works faster (at least should). 
   That's because each device doesn't need to wait for the previous to register.
3. After that, `gather` running programs (in `service.py`) - here the code also may be easy.
   And if you run it — wow, it works so fast, `asyncio` is powerful! But look at the logic —
   we've broken it: we may start playing music on Speaker before it was turned on, 
   same with flushing and cleaning Smart Toilet. So, despite it working fast, it works incorrectly.
4. And finally, your task is to fix these logical problems. 
   As you already have understood, some of these operations may be performed in "parallel", 
   and some of them must still run in a sequence (flush -> clean). 
   So, you may use these helper functions:
    ```python
    from typing import Any, Awaitable
    
    
    async def run_sequence(*functions: Awaitable[Any]) -> None:
        for function in functions:
            await function
    
    
    async def run_parallel(*functions: Awaitable[Any]) -> None:
        await asyncio.gather(*functions)
    ```
   You have to change the `wake_up_program` and `sleep_program` blocks and their run 
   — to the combination of the `run_sequence` and `run_parallel` sending messages to the service to make it more logical. 
   Please do that separately, firstly for `wake_up`, then for `sleep`. 
   
   Hint:
   Remove variables `wake_up_program` and `sleep_program` and `run the programs` block.
   Instead, you should combine `run_sequence` and `run_parallel` with the same commands from `wake_up_program` and `sleep_program`.
   The parallel running is always preferred, because it is faster, but logical order should be taken into account (for ex: switch on -> play; flush -> clean).
   After that, your code will work a bit longer (still faster than at the beginning), 
   but at least it works correctly now.
    
**Please note:** attach the screenshot of your script results (the console) to the PR.


