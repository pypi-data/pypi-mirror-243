class Superclass:
    def some_method(self):
        print("Superclass method")

class Subclass(Superclass):
    def some_method(self):
        print("Subclass method")
        # Call the superclass method
        super().some_method()

# Instantiate the subclass
obj = Subclass()

# Call the overridden method in the subclass
obj.some_method()


exit(1)

from torch.utils.tensorboard import SummaryWriter
import torchvision

# Init writer and model
writer = SummaryWriter('runs/demo')
model = torchvision.models.resnet50()
dummy_data, _ = load_dataset()

# Add model graph
writer.add_graph(model, dummy_data)

# Fake training loop for demo
for epoch in range(5):
    loss = epoch * 0.1  # Simulated loss
    writer.add_scalar('train_loss', loss, epoch)

# Close writer
writer.close()