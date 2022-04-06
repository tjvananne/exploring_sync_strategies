# exploring_sync_strategies

I'm interested in how a tool like Obsidian (one user wanting to sync files across multiple devices) works. For now, all I'll need for this is a very naive copy-all-data type of sync. I am interested in playing with more interesting methods like CRDTs, operational transforms, and possibly something like merkle trees. This might be a good time to explore the WYAG (write-yourself-a-git) project to see how git breaks up large files. I believe that's done through some form of on-disk persistent data structure.

(As a side note, I think CRDTs and operational transforms are better for multi-user, near-real-time environments. That's likely not the right solution for a single-user environment).

I'm thinking this is how I'd like to progress through the various iterations of syncing - not necessarily in this order:

1. sync a source file to a target file on the disk of the same machine (done)
2. bidirectional sync between two files on the disk of the same machine (done)
3. put this bidirectional sync between two files in a background async co-routing
4. sync file data to a server that is constantly accepting data to store on disk. enable two machines to connect to this server so that they can sync data between the two machines (probably going to simulate this on a few VirtualBox VMs - one client and one server and then use my host machine as a second client)
    - at this point, I have to keep in mind that Obsidian is some type of electron app (I think?). I'm not sure how they keep the sync "job" running in the background at all times. Are they checking for changes across all files at all times? This shouldn't be too terribly difficult if you're using hashes for the entire file contents. Especially in a single-user environment.

