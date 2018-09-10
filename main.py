import cmd
from sys import exit
import methods # the main() in methods will be run before this module's main()


class main(cmd.Cmd):

    prompt = '$ '

    def do_list(self, args):
        args_a = args.split(' ')
        if args_a[0] == '-a':
            methods.list_all()
        elif args_a[0] == '-m':
            methods.list_marked_tweets()
        elif args_a[0] == '-rt':
            try:
                methods.list_retweets(args_a[1])
            except:
                try:
                    methods.list_retweets()
                except:
                    print('something went wrong')
        elif args_a[0] == '-rp':
            try:
                methods.list_replies(args_a[1])
            except:
                try:
                    methods.list_replies()
                except:
                    print('something went wrong')
        elif args_a[0] == '-ym':
            try:
                methods.list_by_yr_month(args_a[1:len(args)])
            except:
                print('something went wrong')
        elif args_a[0] == '-h':
            try:
                methods.list_by_hashtag(args_a[1])
            except:
                print('a hashtag must be specified')
        elif args_a[0] == '-k':
            try:
                # define a new args_b that only applies the split once
                # this will allow not only singular words but phrases to be found
                args_b = args.split(' ', 1)
                methods.list_by_keyword(args_b[1])
            except:
                print('a key word/phrase must be specified')
        else:
            print('invalid option')

    def do_setpath(self, arg):
        methods.set_archive_path(arg)

    def do_readcsv(self, _arg):
        try:
            methods.read_csv()
        except:
            print('file not found. try fixing csv path')

    def do_mark(self, args):
        args_a = args.split(' ')
        if args_a[0] == '-i':
            try:
                methods.mark_tweet_by_id(args_a[1])
            except:
                print('something went wrong. make sure you are passing in a valid tweet id')
        elif args_a[0] == '-rt':
            try:
                methods.mark_retweets(args_a[1])
            except:
                try:
                    methods.mark_retweets()
                except:
                    print('something went wrong')
        elif args_a[0] == '-k':
            try:
                # define a new args_b that only applies the split once
                # this will allow not only singular words but phrases to be found
                args_b = args.split(' ', 1)
                methods.mark_by_keyword(args_b[1])
            except:
                print('a key word/phrase must be specified')
        elif args_a[0] == '-rp':
            try:
                methods.mark_replies(args_a[1])
            except:
                try:
                    methods.mark_replies()
                except:
                    print('something went wrong')
        elif args_a[0] == '-h':
            try:
                methods.mark_by_hashtag(args_a[1])
            except:
                print('a hashtag must be specified')
        else:
            print('specify a valid option')

    def do_clear(self, arg):
        args = arg.split(' ')
        if args[0] == '-a':
            methods.clear_marked_tweets()
            print('cleared all marked tweets')
        elif args[0] == '-i':
            try:
                methods.clear_tweet(args[1])
            except:
                print('make sure you are passing in a valid tweet id')
        else:
            print('specify an option')

    def do_nuke(self, _arg):
        methods.delete_markeds()

    def do_curpath(self, _arg):
        methods.output_archive_path()

    # new methods below
    def do_auth(self, _arg):
        methods.authenticate()

    def do_checkauth(self, _arg):
        print(methods.authenticated)

    def do_showkeys(self, _arg):
        methods.list_keys()

    def do_edit(self, arg):
        args = arg.split(' ', 1)
        if args[0] == '-ck':
            try:
                methods.set_consumer_key(args[1])
            except:
                print('a valid option must be specified. check $ help for details')
        elif args[0] == '-cs':
            try:
                methods.set_consumer_secret(args[1])
            except:
                print('a valid option must be specified. check $ help for details')
        elif args[0] == '-ak':
            try:
                methods.set_access_key(args[1])
            except:
                print('a valid option must be specified. check $ help for details')
        elif args[0] == '-as':
            try:
                methods.set_access_secret(args[1])
            except:
                print('a valid option must be specified. check $ help for details')
        else:
            print('a valid option must be specified. check $ help for details')
    # new methods stop
    def do_exit(self, _arg):
        exit()

    def do_help(self, arg):
        print('$ setpath\n\t[path]\tset path of tweet archive')
        print('$ curpath\n\toutputs the current path of the tweet archive')
        print('$ readcsv\n\tread in the csv file at the given path')
        print('$ list')
        print('\t-a\t\tlist all tweets (may not show all depending on number of tweets)')
        print('\t-m\t\tlist all tweets that are marked for deletion')
        print('\t-rt\t\tlist all tweets that are retweets')
        print('\t\t[a] - any user from which to search retweets')
        print('\t-h\t\tlist all tweets that contain a certain hashtag (hashtag not needed in input)')
        print('\t-rp\t\tlist all tweets that are replies')
        print('\t\t[a] - any user from which to search replies')
        print('\t-ym\t\tlist all tweets according to specified year and month')
        print('\t\t-[*a] - any amount of year-month combinations')
        print('\t-k\t\tlist all tweets according to specified keyword(s)')
        print('\t\t-[s] - any keyword(s) to search for. phrases in the form of multiple keywords can also be searched')
        print('$ clear')
        print('\t-a\t\tclear the entire list of marked tweets WITHOUT deletion')
        print('\t-i\t\tclear a specific tweet from the marked list by its tweet id')
        print('\t\t-[a] - tweetid')
        print('$ nuke\n\tdelete all tweets that are marked')
        print('$ mark')
        print('\t-i\t\tmark a tweet with its id')
        print('\t\t[id] - tweet id')
        print('\t-a\t\tmark all tweets (may not show all depending on number of tweets)')
        print('\t-rt\t\tmark all tweets that are retweets')
        print('\t\t[a] - any user from which to mark retweets')
        print('\t-h\t\tmark all tweets that contain a certain hashtag (hashtag not needed in input)')
        print('\t-rp\t\tmark all tweets that are replies')
        print('\t\t[a] - any user from which to mark replies')
        print('\t-ym\t\tmark all tweets according to specified year and month')
        print('\t\t-[*a] - any amount of year-month combinations')
        print('\t-k\t\tmark all tweets according to specified keyword(s)')
        print('\t\t-[s] - any keyword(s) to search for. phrases in the form of multiple keywords can also be searched')
        print('$ auth\n\tauthenticate using supplied keys (see $ edit for details)')
        print('$ edit')
        print('\t-ck\t\tedit consumer_key')
        print('\t\t-[k] - consumer_key value')
        print('\t-cs\t\tedit consumer_secret')
        print('\t\t-[k] - consumer_secret value')
        print('\t-ak\t\tedit access_key')
        print('\t\t-[k] - access_key value')
        print('\t-as\t\tedit access_secret')
        print('\t\t-[k] - access_secret value')
        print('$ checkauth\n\toutput a boolean telling whether authenticated or not')
        print('$ showkeys\n\toutput all authentication keys')
        print('$ exit\n\texit the application')
        print('-----')

    def do_a(self, _arg):
        methods.showinfo()


main().cmdloop()