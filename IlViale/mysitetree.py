from sitetree.sitetreeapp import SiteTree


class MySiteTree(SiteTree):
    """Custom tree handler to test deep customization abilities."""

    def apply_hook(self, items, sender):
        # Suppose we want to process only menu child items.
        if sender == 'menu.children':
            # Lets add 'Hooked: ' to resolved titles of every item.
            for item in items:
                item.title_resolved = 'Hooked: %s' % item.title_resolved
        # Return items list mutated or not.
        return items