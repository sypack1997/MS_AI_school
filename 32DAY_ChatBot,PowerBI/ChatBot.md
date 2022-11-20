# 챗봇 만들기 실습
## 1. 개발환경 구성
1. Visual Studio comuunity edition 설치 https://visualstudio.microsoft.com/ko/vs/community/
2. Bot Emulator download (환경에 맞춰 다운로드)https://github.com/microsoft/BotFramework-Emulator/releases
3. 시작 프로젝트 파일의 다운로드 https://github.com/KoreaEva/Bot/blob/master/HOL/20190629%20Chatbot%20HOL/GreatWall_Start.zip

## 2. Code
1. 메세지 주고 받기
```python
          private async Task MessageReceivedAsync(IDialogContext context, IAwaitable<object> result)
        {
            var activity = await argument as Activity;

            string message = string.Format("{0}을 주문하셨습니다. ", activity.Text);

            await context.PostAsync(message);

            context.Wait(MessageReceivedAsync);
        }
```
2. 인사기능 구현
```python  
          private async Task MessageReceivedAsync(IDialogContext context, IAwaitable<object> result)
        {
            await context.PostAsync("안녕하세요 신속배달 만리장성 봇 입니다. 주문하시려는 음식을 입력해 주세요");

            context.Wait(SendWelcomeMessageAsync);
        }
```        
3. 인사 기능 구현2
```python
          private async Task SendWelcomeMessageAsync(IDialogContext context, IAwaitable<object> result)
        {
            var activity = await result as Activity;

            string message = string.Format("{0}을 주문하셨습니다. 감사합니다.", activity.Text);
            await context.PostAsync(message);

            context.Wait(SendWelcomeMessageAsync);
        }
```        
4. Dialog 구현
```python
  	string WelcomeMessage = "안녕하세요 만리장석 봇입니다. 1.주문 2.FAQ 중에 선택하세요";
	
        private async Task SendWelcomeMessageAsync(IDialogContext context, IAwaitable<object> result)
        {
            var activity = await result as Activity;
            string selected = activity.Text.Trim();

            if (selected == "1")
            {
                await context.PostAsync("음식 주문 메뉴 입니다. 원하시는 음식을 입력해 주십시오.");
                context.Call(new OrderDialog(), DialogResumeAfter);
            }
            else if (selected == "2")
            {
                await context.PostAsync("FAQ 서비스 입니다. 질문을 입력해 주십시오.");
                context.Call(new FAQDialog(), DialogResumeAfter);
                
            }
            else
            {
                await context.PostAsync("잘못 선택하셨습니다. 다시 선택해 주십시오");
                context.Wait(SendWelcomeMessageAsync);
            }
            
        }
```        
5. Order Dialog
```python
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

using System.Threading.Tasks;
using Microsoft.Bot.Connector;
using Microsoft.Bot.Builder.Dialogs;

namespace GreatWall.Dialogs
{
    [Serializable]
    public class OrderDialog : IDialog<string>
    {
        public Task StartAsync(IDialogContext context)
        {
            context.Wait(MessageReceivedAsync);

            return Task.CompletedTask;
        }

        private async Task MessageReceivedAsync(IDialogContext context, IAwaitable<object> result)
        {
            var activity = await result as Activity;

            if (activity.Text.Trim() == "그만")
            {
                context.Done("주문완료");
            }
            else
            {
                string message = string.Format("{0}을 주문하셨습니다. 감사합니다.", activity.Text);

                await context.PostAsync(message);

                context.Wait(MessageReceivedAsync);
            }
        }
    }
}
```
6. DialogResumeAfter() 추가
```python
          private async Task DialogResumeAfter(IDialogContext context, IAwaitable<string> result)
        {
            try
            {
                string message = await result;

		await this.MessageReceivedAsync(context, result);
            }
            catch (TooManyAttemptsException)
            {
                await context.PostAsync("오류가 생겼습니다. 죄송합니다.");
            }
        }
```  
7. 최종
```python  
  using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

using System.Threading.Tasks;
using Microsoft.Bot.Connector;
using Microsoft.Bot.Builder.Dialogs;

namespace GreatWall.Dialogs
{
    [Serializable]
    public class FAQDialog : IDialog<string>
    {
        public Task StartAsync(IDialogContext context)
        {
            context.Wait(MessageReceivedAsync);

            return Task.CompletedTask;
        }

        private async Task MessageReceivedAsync(IDialogContext context, IAwaitable<object> result)
        {
            var activity = await result as Activity;

            if (activity.Text.Trim() == "그만")
            {
                context.Done("주문완료");
            }
            else
            {
                await context.PostAsync("FAQ Dialog 입니다.");

                context.Wait(MessageReceivedAsync);
            }
        }
    }
}
```  
8. Card 형태의 RootDiaglog.cs
```python  
  	using System.Collections.Generic;


        private async Task MessageReceivedAsync(IDialogContext context, IAwaitable<object> result)
        {
            await context.PostAsync(WelcomeMessage);

            var message = context.MakeMessage();

            var actions = new List<CardAction>();

            actions.Add(new CardAction() { Title = "1.주문", Value = "1" , Type = ActionTypes.ImBack });
            actions.Add(new CardAction() { Title = "2.FAQ", Value = "2" , Type = ActionTypes.ImBack });


            message.Attachments.Add(
                new HeroCard
                {
                    Title = "원하는 기능을 선택하세요",
                    Buttons = actions
                }.ToAttachment()
            );

            await context.PostAsync(message);

            context.Wait(SendWelcomeMessageAsync);
        }
```
