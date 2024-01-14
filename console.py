#!/usr/bin/python3
""" Defines the console class
which is the entry point of the Airbnb Project
"""


from cmd import Cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = ("BaseModel",
           "User",
           "State",
           "City",
           "Amenity",
           "Place",
           "Review")


class ModelNotFoundError(Exception):
    """Raised when an unknown module is passed"""
    def __init__(self, arg="BaseModel"):
        super().__init__(f"Model with name {arg} is not registered!")


class InstanceNotFoundError(Exception):
    """Raised when an unknown id  is passed"""

    def __init__(self, obj_id="", mod="BaseModel"):
        super().__init__(f"Insatnce of {mod} with id {obj_id} does not exist!")


class HBNBCommand(Cmd):
    """ the prompt for hbnb """
    prompt = "(hbnb) "
    # controling units

    def do_EOF(self, arg):
        """Exits the programme"""
        return True

    def do_quit(self, arg):
        """quit the program"""
        return True

    def emptyline(self):
        """Overides empty line to do nothing """
        pass

    def do_create(self, arg):
        """creates various instances for the previous classes
        we already created for the program.
        $ create (classname) prints the id if it is correct and error if not
        """
        args = arg.split()
        n = len(args)

        if not n:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif n == 1:
            tmp = eval(args[0])()
            print(tmp.id)
            tmp.save()
        else:
            print("** Too many argument for create **")
            pass

    def do_show(self, arg):
        """show the the class with the same id entered.
        $ show (myclass) myclass.id
        prints the class with the same id and error if not found """
        args = arg.split()
        n = len(args)
        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            try:
                myclass = storage.id_finder(*args)
                print(myclass)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for show **")
            pass

    def do_destroy(self, arg):
        """deletes a class with the same id given."""
        arg = args.split()
        n = len(args)
        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            try:
                storage.id_destroyer(*args)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for destroy **")
            pass

    def do_all(self, arg):
        """it prints all the classes or instances that is saved in."""
        args = arg.split()
        n = len(args)
        if n < 2:
            try:
                print(storage.allfinder(*args))
            except ModelNotFoundError:
                print("** class doesn't exist **")
        else:
            print("** Too many argument for all **")
            pass

    def do_update(self, arg):
        """Updates the instance with id.
        $ update (class) id: updates the class if works otherwise
        Throws errors for missing arguments"""
        args = arg.split()
        n = len(args)
        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            print("** attribute name missing **")
        elif n == 3:
            print("** value missing **")
        else:
            try:
                storage.updater(*args[0:4])
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")

    def default(self, arg):
        """Override default method"""
        if '.' in arg and arg[-1] == ')':
            if arg.split('.')[0] not in classes:
                print("** class doesn't exist **")
                return
            return self.handler(arg)
        return Cmd.default(self, arg)

    def do_models(self, arg):
        """Print all registered Models"""
        print(*classes)

    def handler(self, arg):
        """Handle Class Methods in advanced tasks :'(
        """
        printers = ("all(", "show(", "count(", "create(")
        try:
            val = eval(arg)
            for x in printers:
                if x in arg:
                    print(val)
                    break
            return
        except AttributeError:
            print("** invalid method **")
        except InstanceNotFoundError:
            print("** no instance found **")
        except TypeError as te:
            field = te.args[0].split()[-1].replace("_", " ")
            field = field.strip("'")
            print(f"** {field} missing **")
        except Exception as e:
            print("** invalid syntax **")
            pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
