
import os
import stat

_priv_flags_ = {
                  'r' : ( stat.S_IRUSR , stat.S_IRGRP , stat.S_IROTH ) ,
                  'w' : ( stat.S_IWUSR , stat.S_IWGRP , stat.S_IWOTH ) ,
                  'x' : ( stat.S_IXUSR , stat.S_IXGRP , stat.S_IXOTH ) 
               }


def eaccess( path , mode ):
    if not mode in _priv_flags_:
        raise KeyError( "Invalid mode value %s specified. Valid values are [%s]" %
                               ( mode , '|'.join( _priv_flags_.keys() ) ) )
    try:
       flags = _priv_flags_[ mode ]
       st = os.stat( path )
       if os.geteuid() == st.st_uid and st.st_mode & flags[ 0 ] :
           return True
       for grp in os.getgroups():
           if grp == st.st_gid and st.st_mode & flags[ 1 ]:
               return True
       if st.st_mode & flags[ 2 ]:
           return True

    except OSError:
        return False


def is_readable( path ):
    return eaccess( path , 'r' )

def is_writeable( path ):
    return eaccess( path , 'w' )

def is_executable( path ):
    return eaccess( path , 'x' )


if __name__ == '__main__':
    import sys

    if len( sys.argv ) != 2:
        sys.stderr.write( "Usage: %s path\n" % ( os.path.basename( sys.argv[ 0 ] ) ) )
        sys.exit( 1 )
        
    f = sys.argv[ 1 ]

    if is_readable( f ):
        print( "%s is readable" % ( f ) )
    if is_writeable( f ):
        print( "%s is writeable" % ( f ) )
    if is_executable( f ):
        print( "%s is executable" % ( f ) )
