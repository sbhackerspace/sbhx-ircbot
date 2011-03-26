// Steve Phillips / elimisteve
// 2011.03.25

package main

import (
    "fmt"
    "net"
    "os"
    "strings"
)

const (
    BOT_NICK    = "sbhx-gitgo"
    IRC_SERVER  = "irc.freenode.net:6667"
    IRC_CHANNEL = "#sbhackerspace"
)

func ircSetup() (c net.Conn, e os.Error) {
    //IRC_CHANNELS := []string{"#sbhackerspace"}
    conn, err := net.Dial("tcp", "", IRC_SERVER)
    if err == nil {
        ircMsg(conn, "NICK " + BOT_NICK)
        ircMsg(conn, "USER " + strings.Repeat(BOT_NICK+" ", 4))
        ircMsg(conn, "JOIN " + IRC_CHANNEL)
        // for _, channel := range IRC_CHANNELS {
        //     ircMsg(conn, "JOIN " + channel)
        // }
    }
    return conn, err
}

func main() {
    conn, err := ircSetup()
    if err != nil {
        fmt.Printf("Error: %v\n", err)
    } else {
        fmt.Printf("Remote Address: %v\n", conn.RemoteAddr())
                //
                // Main loop
        for {   //
            read_buf := make([]byte, 512)
            length, err := conn.Read(read_buf)
            if err != nil {
                fmt.Printf("Error: %v\n", err)
                conn.Close()
                os.Exit(1)
            } else {
                msg := string(read_buf[:length])
                fmt.Printf("%v\n", msg)
                //
                // Respond to PING
                //
                if strings.HasPrefix(msg, "PING") {
                    ircMsg(conn, "PONG " + msg)
                    fmt.Printf("PONG\n")
                }
                //
                // Parse nick
                //
                if strings.Contains(msg, "PRIVMSG") {
                    nick := strings.Split(msg, "!", 2)[0][1:] // I love Go
                    fmt.Printf("Sent by " + nick)
                }
                //
                // Parse msg
                //

                /*
                 *  Future code goes here
                 */
            }
        }
    }
}

func ircMsg(c net.Conn, str string) {
    c.Write([]uint8(str+"\n"))
}
