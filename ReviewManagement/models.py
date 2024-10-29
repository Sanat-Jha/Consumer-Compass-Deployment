from django.db import models

# Create your models here.
class Review(models.Model):
    content = models.TextField()
    product = models.ForeignKey('ProductManagement.Product', on_delete=models.CASCADE)
    consumer = models.ForeignKey('UserManagement.Consumer', on_delete=models.CASCADE)
    approvallist = models.JSONField(default=list)  # List of strings of usernames
    approvalscore = models.IntegerField(default=0)

    def toggle_approval(self, username):
        # Check if the username has already approved
        if username not in self.approvallist:
            # Add the username to the approvallist
            self.approvallist.append(username)
            # Increase approvalscore by 1
            self.approvalscore += 1
            # Save the updated Review instance
            self.save()

            # Update the approvedscore for the consumer related to the review
            self.consumer.approvedscore += 1
            # Save the updated Consumer instance
            self.consumer.save()
        else:
            # Remove the username from the approvallist
            self.approvallist.remove(username)
            # Decrease approvalscore by 1
            self.approvalscore -= 1
            # Save the updated Review instance
            self.save()

            # Update the approvedscore for the consumer related to the review
            self.consumer.approvedscore -= 1
            # Save the updated Consumer instance
            self.consumer.save()


    def __str__(self):
        return self.content[:50]  # Return the first 50 characters of the review content
