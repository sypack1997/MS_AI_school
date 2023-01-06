import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_csv("modelAccuracy.csv")


print(df.head(5))


epochs = df["Epoch"]
train_acc = df["train_Accuracy"]
val_acc = df["val_Accuracy"]
train_loss =df["train_loss"]
val_loss = df["val_loss"]


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14,5))
ax[0].plot(train_acc, color='r', label="train_acc")
ax[0].plot(val_acc, color='b', label="va_acc")
ax[0].set_title('Trianing and validation accuracy')
ax[0].legend()

ax[1].plot(train_loss, color='r', label="train_loss")
ax[1].plot(val_loss, color='b', label="val_loss")
ax[1].set_title('Trianing and validation loss')
ax[1].legend()
plt.tight_layout()
plt.show()