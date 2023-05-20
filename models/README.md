# Code Well

Users Table:
        Fields:
            ID (integer)
            Username (string)
            Email (string)
            Password (string, encrypted)
            Name (string)
            Gender (string)
            Registration Date (datetime)
            Last Login (datetime)

    Repositories Table:
        Fields:
            ID (integer)
            Name (string)
            Description (string)
            Owner ID (integer, foreign key referencing Users table)
            Creation Date (datetime)

    Tasks Table:
        Fields:
            ID (integer)
            Title (string)
            Description (string)
            Assignee ID (integer, foreign key referencing Users table)
            Due Date (date)
            Status (string)

    Blog Posts Table:
        Fields:
            ID (integer)
            Title (string)
            Content (text)
            Author ID (integer, foreign key referencing Users table)
            Publication Date (datetime)

    Health Articles Table:
        Fields:
            ID (integer)
            Title (string)
            Content (text)
            Author ID (integer, foreign key referencing Users table)
            Publication Date (datetime)

    GitHub Info Table:
        Fields:
            ID (integer)
            User ID (integer, foreign key referencing Users table)
            Repositories (integer)
            Followers (integer)
            Stars (integer)
            Description (text)