# Import necessary modules from Kivy
import kivy
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from buttonlist import button_list
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.pagelayout import PageLayout

# Set the minimum version of Kivy required
kivy.require('1.9.0')

class BoxLayoutMain(BoxLayout):
    def update_debug_info(self):
        scroll_view = self.ids.scroll_view
        scroll_y = scroll_view.scroll_y
        container = self.ids.container
        button_height = MyApp.button_height

        # Calculate the index of the first visible button
        first_visible_index = int(scroll_y * len(container.children))

        # Calculate the index of the last visible button
        last_visible_index = int((scroll_y + scroll_view.height / container.height) * len(container.children))

        # Ensure that the indices are within bounds
        if first_visible_index < len(container.children):
            first_button_text = container.children[first_visible_index].text
        else:
            first_button_text = "None"

        if last_visible_index < len(container.children):
            last_button_text = container.children[last_visible_index].text
        else:
            last_button_text = "None"

        print(f"First visible button index: {first_visible_index}")
        print(f"Last visible button index: {last_visible_index}")
        print(f"Text of first visible button: {first_button_text}")
        print(f"Text of last visible button: {last_button_text}")

        # Update the image based on the first visible button text
        self.update_image(first_button_text)

    def update_image(self, text):
        # Find the corresponding image source in button_list
        for button_tuple in button_list:
            if button_tuple[0] == text:
                image_source = button_tuple[2]
                break
        else:
            # Set a default image source if no matching text is found
            image_source = 'map/default_map.png'

        # Update the image source in the CustomImage widget
        self.ids.custom_image.source = image_source
        
class OverlayLayout(RelativeLayout):
    pass

class CustomImage(Image):
    def __init__(self, **kwargs):
        super(CustomImage, self).__init__(**kwargs)
        self.source = 'map/default_map.png'
        self.allow_stretch = True
        self.keep_ratio = False
        self.size_hint = (1, 1)

class CustomSiteButton(Button):
    background_normal = StringProperty('data/btn-rd1.png')
    background_down = StringProperty('data/btn-rd2.png')  

    def __init__(self, **kwargs):
        super(CustomSiteButton, self).__init__(**kwargs)
        self.size_hint = (0.9, None)
        self.height = dp(38)
        self.pos_hint = {'center_x': 0.5}
        self.background_size = (self.width, self.height)
        self.font_size = '20sp'
        self.popup_instance = None  # Store a reference to the popup instance

    def show_popup(self, text):
        # Find the corresponding image source in button_list
        for button_tuple in button_list:
            if button_tuple[0] == text:
                # Construct the full path to the image using the App's directory
                image_source = button_tuple[1]
                break
        else:
            # If no matching text is found, set the default image source
            image_source = 'layout/default_layout.png'
            
        popup_content = LayoutPopup(image_source=image_source)
        popup = Popup(title=text, content=popup_content, size_hint=(1, 1))
        popup.open()
        
'''
class LayoutPopup(BoxLayout):
    image_source = StringProperty()  # Define the image_source property
    
    def __init__(self, **kwargs):
        super(LayoutPopup, self).__init__(**kwargs)
        self.orientation = 'vertical'  # Set the orientation of the BoxLayout
        
        # Image widget at the top
        image = Image(source=self.image_source, size_hint=(1, 0.8), allow_stretch=True, keep_ratio=True)
        self.add_widget(image)
        
        # Button at the bottom
        dismiss_button = Button(text='OK', size_hint=(1, None), height=dp(40))
        dismiss_button.bind(on_release=self.dismiss_popup)  # Bind the button to the dismiss_popup method
        self.add_widget(dismiss_button)

    def dismiss_popup(self, instance):
        # Traverse the widget tree to find the parent popup and dismiss it
        parent_widget = self.parent
        while not isinstance(parent_widget, Popup):
            parent_widget = parent_widget.parent

        parent_widget.dismiss()
'''

class LayoutPopup(PageLayout):
    image_source = StringProperty()  # Define the image_source property
    
    def __init__(self, **kwargs):
        super(LayoutPopup, self).__init__(**kwargs)
        
        # Create and add the site layout page
        self.add_site_layout_page()
        
        # Create and add the managers page
        self.add_managers_page()
        
        # Create and add the boats page
        self.add_boats_page()
        
        # Create and add the tide page
        self.add_tide_page()

        # Create and add the weather page
        self.add_weather_page()

    def add_site_layout_page(self):
        site_layout = BoxLayout(orientation='vertical')
        
        # Image widget at the top
        image = Image(source=self.image_source, size_hint=(1, 0.8), allow_stretch=True, keep_ratio=True)
        site_layout.add_widget(image)
        
        # Button at the bottom
        dismiss_button = Button(text='OK', size_hint=(1, None), height=dp(40))
        dismiss_button.bind(on_release=self.dismiss_popup)  # Bind the button to the dismiss_popup method
        site_layout.add_widget(dismiss_button)
        
        self.add_widget(site_layout)
        
    def add_managers_page(self):
        managers_page = BoxLayout(orientation='vertical')
        
        managers_button = Button(text='Managers', size_hint=(1, 1))
        managers_page.add_widget(managers_button)
        
        self.add_widget(managers_page)
        
    def add_boats_page(self):
        boats_page = BoxLayout(orientation='vertical')
        
        boats_button = Button(text='Boats', size_hint=(1, 1))
        boats_page.add_widget(boats_button)
        
        self.add_widget(boats_page)
        
    def add_tide_page(self):
        tide_page = BoxLayout(orientation='vertical')
        
        tide_button = Button(text='Tide', size_hint=(1, 1))
        tide_page.add_widget(tide_button)
        
        self.add_widget(tide_page)
    
    def add_weather_page(self):
        weather_page = BoxLayout(orientation='vertical')
        
        weather_button = Button(text='Weather', size_hint=(1, 1))
        weather_page.add_widget(weather_button)
        
        self.add_widget(weather_page)
        
    def dismiss_popup(self, instance):
        # Traverse the widget tree to find the parent popup and dismiss it
        parent_widget = self.parent
        while not isinstance(parent_widget, Popup):
            parent_widget = parent_widget.parent

        parent_widget.dismiss()
        
class CustomExitButton(Button):
    background_normal = StringProperty('data/exit1.png')
    background_down = StringProperty('data/exit2.png')  

    def __init__(self, **kwargs):
        super(CustomExitButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = ('40dp', '40dp')
        self.pos_hint = {'x': 0, 'top': 1}
        self.bind(on_release=self.on_button_release)

    def on_button_release(self, *args):
        # Call the exit_confirmation method from the MyApp instance
        app_instance = App.get_running_app()
        app_instance.exit_confirmation()


class MyApp(App):
    button_height = dp(38)

    def exit_confirmation(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Do you want to exit the application?', size_hint=(1, 1)))
        btn_layout = BoxLayout()

        # Adjust button height here
        btn_yes = Button(text='Yes', size_hint=(1, 0.7))
        btn_yes.bind(on_press=self.exit_app)  # Bind the "Yes" button to exit_app method

        # Adjust button height here
        btn_no = Button(text='No', size_hint=(1, 0.7))
        btn_no.bind(on_press=self.dismiss_popup)

        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)
        content.add_widget(btn_layout)

        self.popup = Popup(title='Exit Confirmation', content=content, size_hint=(0.8, 0.4))
        self.popup.open()

    def exit_app(self, instance):
        self.stop()  # Stop the application

    def dismiss_popup(self, instance):
        self.popup.dismiss()

    def build(self):
        return BoxLayoutMain()

    def on_start(self):
        # Import button list here
        button_list_path = os.path.join(os.path.dirname(__file__), 'buttonlist.py')
        if os.path.exists(button_list_path):
            globals().update(__import__('buttonlist').__dict__)


if __name__ == "__main__":
    # Create the root widget
    root = MyApp()

    # Bind the Kivy app to the root widget
    root.run()
